from flask import Flask, render_template
from app import app_bp, UPLOAD_FOLDER
from ext import db
import os

from excel_sync import import_from_excel, export_to_excel
EXCEL_FILE = 'students.xlsx'
app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_bp)

# Configure upload folder to an absolute path under the app's static dir so
# templates that reference static files continue to work.
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db.co'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def ensure_app_data():
    # Ensure the configured upload directory exists (absolute path)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if os.path.exists(EXCEL_FILE):
            imported = import_from_excel(EXCEL_FILE)
            print(f'[excel_sync] Imported {imported} rows from {EXCEL_FILE}')


@app.route('/export_excel')
def export_excel_route():
    exported = export_to_excel(EXCEL_FILE)
    return f'Exported {exported} students to {EXCEL_FILE}'
@app.route('/')
def main_page():
    return render_template('main.html')


if __name__ == '__main__':
    ensure_app_data()
    app.run(host='0.0.0.0', port=5000, debug=False)