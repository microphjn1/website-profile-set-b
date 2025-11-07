from main import app
from ext import db
from sqlalchemy import inspect

# Initialize the db extension with the app and create tables (if missing)
# Run this from the project root (so imports work)

db.init_app(app)
with app.app_context():
    db.create_all()
    insp = inspect(db.engine)
    print('TABLES:', insp.get_table_names())
    print('DB URL:', db.engine.url)
