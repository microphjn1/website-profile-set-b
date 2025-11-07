"""Migrate data from legacy 'students' table to SQLAlchemy 'Student' table and drop legacy table."""
import os
import sys
import sqlite3

proj_root = os.path.dirname(__file__)
proj_root = os.path.dirname(proj_root)
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from main import app
from ext import db
from models import Student

DB_PATH = os.path.join(proj_root, 'instance', 'students.db')

db.init_app(app)
with app.app_context():
    # read from legacy table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        if 'students' not in tables:
            print('No legacy students table found. Nothing to do.')
        else:
            cur.execute('SELECT * FROM students')
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            print('Found', len(rows), 'rows in legacy students table, columns:', cols)
            copied = 0
            for row in rows:
                rowd = dict(zip(cols, row))
                name = rowd.get('name') or rowd.get('Name')
                if not name:
                    continue
                name = str(name).strip()
                exists = Student.query.filter_by(name=name).first()
                if exists:
                    continue
                s = Student(
                    name=name,
                    course=rowd.get('course'),
                    hobbies=rowd.get('hobbies'),
                    languages=rowd.get('languages'),
                    motto=rowd.get('motto'),
                    career_interests=rowd.get('career_interests') or rowd.get('career'),
                    reason=rowd.get('reason'),
                    picture=rowd.get('picture'),
                )
                db.session.add(s)
                copied += 1
            if copied:
                db.session.commit()
                print('Copied', copied, 'rows into Student model')
            else:
                print('No new rows copied')

            # drop legacy table
            cur.execute('DROP TABLE IF EXISTS students')
            conn.commit()
            print('Dropped legacy table students')
    finally:
        conn.close()

print('Migration complete')
