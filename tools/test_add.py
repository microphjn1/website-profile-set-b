import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, ensure_app_data
from models import Student

ensure_app_data()
with app.app_context():
    # remove any previous test entries
    Student.query.filter_by(name='Form Tester').delete()
    from ext import db
    db.session.commit()

c = app.test_client()
r = c.post('/add', data={'name':'Form Tester','course':'BSIT','hobbies':'','languages':'Python','motto':'','reason':'test','career':['Software','AI']}, follow_redirects=True)
print('status', r.status_code)
with app.app_context():
    s = Student.query.filter_by(name='Form Tester').first()
    if s:
        print('Created:', s.id, s.name, s.career_interests)
    else:
        print('Student not found')
