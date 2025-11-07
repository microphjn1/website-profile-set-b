"""
Merge SQLite DB files into the canonical DB used by Flask-SQLAlchemy.

This script will:
- Use the Flask app and ext.db (SQLAlchemy) as the target DB (instance/students.db)
- For each source DB path provided, open it via sqlite3 and try to read tables named 'Student' or 'students'
- Map columns to the Student model fields and insert rows that don't already exist (by name)

Run from project root:
    python tools\merge_dbs.py

This is a safe, idempotent merge that avoids creating duplicates by checking names.
"""
import os
import sqlite3
from datetime import datetime
import sys

# ensure project root is importable
proj_root = os.path.dirname(__file__)  # tools
proj_root = os.path.dirname(proj_root)
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from main import app
from ext import db
from models import Student

SOURCE_DBS = [
    os.path.join(proj_root, 'student.db'),
    os.path.join(proj_root, 'templates', 'student.db'),
]

copied = 0

db.init_app(app)
with app.app_context():
    os.makedirs(os.path.join(proj_root, 'instance'), exist_ok=True)
    db.create_all()

    for src in SOURCE_DBS:
        if not os.path.exists(src):
            print('source not found, skipping', src)
            continue
        print('processing source db:', src)
        try:
            conn = sqlite3.connect(src)
            cur = conn.cursor()
            # find a Student-like table
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            candidates = [t for t in tables if t.lower() in ('student', 'students')]
            if not candidates:
                print(' no student table found in', src, 'tables:', tables)
                conn.close()
                continue
            table = candidates[0]
            cur.execute(f"SELECT * FROM {table};")
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
            print('  found table', table, 'columns:', cols, 'rows:', len(rows))

            for row in rows:
                rowd = dict(zip(cols, row))
                name = rowd.get('name') or rowd.get('Name')
                if not name:
                    continue
                name = str(name).strip()
                # skip if exists by name
                exists = Student.query.filter_by(name=name).first()
                if exists:
                    continue
                s = Student(
                    name=name,
                    course=rowd.get('course') or rowd.get('Course'),
                    hobbies=rowd.get('hobbies') or rowd.get('Hobbies'),
                    languages=rowd.get('languages') or rowd.get('Languages'),
                    motto=rowd.get('motto') or rowd.get('Motto'),
                    career_interests=rowd.get('career_interests') or rowd.get('career_interests') or rowd.get('career'),
                    reason=rowd.get('reason') or rowd.get('Reason'),
                    picture=rowd.get('picture') or rowd.get('Picture'),
                )
                # try parse created_at if present
                if 'created_at' in rowd and rowd.get('created_at'):
                    try:
                        s.created_at = datetime.fromisoformat(rowd.get('created_at'))
                    except Exception:
                        pass
                db.session.add(s)
                copied += 1
            conn.close()
        except Exception as e:
            print(' failed to read', src, 'error:', e)

    if copied:
        db.session.commit()

print('copied rows:', copied)

# After review, user can delete SOURCE_DBS files manually or script can remove them.
print('Done. You may delete the old DB files:', SOURCE_DBS)
