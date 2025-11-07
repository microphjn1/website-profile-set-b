from main import app
from ext import db
from sqlalchemy import inspect
from models import Student

with app.app_context():
    insp = inspect(db.engine)
    print('Tables:', insp.get_table_names())
    try:
        print('Student count:', db.session.query(Student).count())
    except Exception as e:
        print('Counting students failed:', e)