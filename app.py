from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, session, current_app
import os
from werkzeug.utils import secure_filename
from models import Student
from ext import db



app_bp = Blueprint("app_bp", __name__, template_folder='templates')

# Keep a small list of common extensions but also accept any file whose
# reported MIME type begins with 'image/'. This allows HEIC/WEBP/SVG/etc.
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg', 'tif', 'tiff', 'ico', 'heic', 'avif'}
# default relative path (kept for backward-compat) -- main.py will set an
# absolute path on app.config['UPLOAD_FOLDER'] when the Flask app is created.
UPLOAD_FOLDER = 'static/uploads'  # exported for main.py to configure


def allowed_file(file_or_filename):
    """
    Accept either a FileStorage-like object (has .mimetype and .filename) or
    a filename string. Return True if the extension is known or the
    uploaded file's mimetype starts with 'image/'.
    """
    # If user passed the werkzeug file object, prefer its mimetype
    if hasattr(file_or_filename, 'mimetype'):
        mimetype = getattr(file_or_filename, 'mimetype', '') or ''
        if mimetype.startswith('image/'):
            return True
        filename = getattr(file_or_filename, 'filename', '')
    else:
        filename = file_or_filename or ''

    if not filename:
        return False

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def students_for(term):
    """Return list of dicts for students whose career_interests match term (case-insensitive)."""
    # use ilike for partial/case-insensitive matching
    return [s.to_dict() for s in Student.query.filter(Student.career_interests.ilike(f"%{term}%")).all()]


@app_bp.route('/home')
def home_page():
    # Support optional search query via ?query=...
    q = request.args.get('query', '').strip()
    if q:
        pattern = f"%{q}%"
        results = Student.query.filter(
            (Student.name.ilike(pattern)) |
            (Student.course.ilike(pattern)) |
            (Student.hobbies.ilike(pattern)) |
            (Student.languages.ilike(pattern))
        ).order_by(Student.id).all()
    else:
        results = Student.query.order_by(Student.id).all()
    students = {s.id: s.to_dict() for s in results}
    return render_template('home.html', students=students, query=q)


@app_bp.route('/about')
def about():
    return render_template('about.html')


@app_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app_bp.route('/save_career_interest', methods=['POST'])
def save_career_interest():
    career = request.form.get('career')
    # TODO: get student_id from session or request
    student_id = None
    if student_id is None:
        return redirect(url_for('app_bp.career_page'))
    student = Student.query.get(student_id)
    if student:
        student.career_interests = career
        db.session.commit()
    return redirect(url_for('app_bp.career_page'))


@app_bp.route('/career')
def career_page():
    return render_template('career.html')


@app_bp.route('/software')
def software():
    student = students_for('Software')
    return render_template('soft.html', student=student)


@app_bp.route('/database')
def data_base():
    student = students_for('Database')
    return render_template('database.html', student=student)


@app_bp.route('/ai')
def ai():
    student = students_for('AI')
    return render_template('ai.html', student=student)


@app_bp.route('/cyber')
def cyber():
    student = students_for('Cyber')
    return render_template('cyber.html', student=student)


@app_bp.route('/data_scientist')
def data_scientist():
    student = students_for('Data Scientist')
    return render_template('datascientist.html', student=student)


@app_bp.route('/designer')
def designer():
    student = students_for('Designer')
    return render_template('designer.html', student=student)


@app_bp.route('/mobile')
def mobile():
    student = students_for('Mobile')
    return render_template('mobile.html', student=student)


@app_bp.route('/support')
def support():
    student = students_for('IT Support')
    return render_template('support.html', student=student)


@app_bp.route('/cloud')
def cloud():
    student = students_for('Cloud')
    return render_template('cloud.html', student=student)


@app_bp.route('/business')
def business():
    student = students_for('Business')
    return render_template('business.html', student=student)


@app_bp.route('/tester')
def tester():
    student = students_for('Tester')
    return render_template('tester.html', student=student)


@app_bp.route('/consultant')
def consultant():
    student = students_for('Consultant')
    return render_template('consultant.html', student=student)


@app_bp.route('/devOps')
def Devops():
    student = students_for('DevOps')
    return render_template('devOps.html', student=student)


@app_bp.route('/analyst')
def analyst():
    student = students_for('Analyst')
    return render_template('data_analyst.html', student=student)


@app_bp.route('/Administrator')
def Administrator():
    student = students_for('Administrator')
    return render_template('data_admin.html', student=student)


@app_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve uploaded files from the configured upload folder. Use an absolute
    # path to avoid ambiguity.
    upload_dir = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
    # If upload_dir is relative, make it absolute relative to the app root.
    if not os.path.isabs(upload_dir):
        upload_dir = os.path.join(current_app.root_path, upload_dir)
    return send_from_directory(upload_dir, filename)


@app_bp.route('/profile/<int:student_id>')
def profile(student_id):
    s = Student.query.get_or_404(student_id)
    return render_template('profile.html', student=s.to_dict(), student_id=student_id)


@app_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = {k: request.form.get(k, '').strip() for k in
                ['name', 'course', 'hobbies', 'languages', 'motto', 'reason']}
        file = request.files.get('picture')
        # default to the project's logo if no picture uploaded
        filename = 'image/icct.png'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
        student = Student(
            name=data.get('name') or 'Unnamed',
            course=data.get('course'),
            hobbies=data.get('hobbies'),
            languages=data.get('languages'),
            motto=data.get('motto'),
            reason=data.get('reason'),
            picture=filename,
        )
        # handle career interests from add form
        careers = request.form.getlist('career')
        if careers:
            student.career_interests = ', '.join(careers)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('app_bp.home_page'))
    return render_template('add.html')


@app_bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    s = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        for k in ['name', 'course', 'hobbies', 'languages', 'motto', 'reason']:
            val = request.form.get(k, '').strip()
            setattr(s, k, val)
        # handle career interests (checkboxes can submit multiple values)
        careers = request.form.getlist('career')
        if careers:
            s.career_interests = ', '.join(careers)
        else:
            # if none selected, clear the field
            s.career_interests = None
        file = request.files.get('picture')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = current_app.config.get('UPLOAD_FOLDER', UPLOAD_FOLDER)
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, filename))
            s.picture = filename
        db.session.commit()
        return redirect(url_for('app_bp.profile', student_id=student_id))
    return render_template('edit.html', student=s.to_dict(), student_id=student_id)


@app_bp.route('/delete/<int:student_id>', methods=['POST'])
def delete(student_id):
    s = Student.query.get(student_id)
    if s:
        db.session.delete(s)
        db.session.commit()
    return redirect(url_for('app_bp.home_page'))