import os
import shutil
import uuid
import urllib.request
import urllib.parse
import pandas as pd
from flask import current_app
from ext import db
from models import Student

def import_from_excel(path, commit=True):
    """
    Read an .xlsx file and upsert rows to the Student table.
    Expected columns (case-insensitive): id, name, course, hobbies, languages,
    motto, career_interests, reason, picture, created_at
    Returns number of rows processed.
    """
    if not os.path.exists(path):
        return 0

    # read using openpyxl engine
    df = pd.read_excel(path, engine='openpyxl')
    processed = 0

    for _, row in df.iterrows():
        # skip rows without a name
        name = row.get('name') if 'name' in row else None
        if pd.isna(name) or not str(name).strip():
            continue

        sid = None
        if 'id' in row and not pd.isna(row['id']):
            try:
                sid = int(row['id'])
            except Exception:
                sid = None

        # upsert by id if present, else try by name
        s = None
        if sid:
            s = Student.query.get(sid)
        if not s:
            s = Student.query.filter_by(name=str(name).strip()).first()

        if not s:
            s = Student(name=str(name).strip())

        # helper to normalize cell values
        def val(col):
            if col in row and not pd.isna(row[col]):
                return row[col]
            return None

        s.course = val('course')
        s.hobbies = val('hobbies')
        s.languages = val('languages')
        s.motto = val('motto')
        s.career_interests = val('career_interests')
        s.reason = val('reason')
        pic_val = val('picture')
        # If a picture value is present, try to resolve it into a file
        # stored under the app's configured upload folder. This supports:
        # - HTTP/HTTPS URLs (will be downloaded)
        # - absolute or relative local file paths (will be copied)
        # - bare filenames (left as-is if already present under static/uploads)
        def process_picture(value):
            if not value:
                return None
            try:
                s = str(value).strip()
            except Exception:
                return None

            upload_dir = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
            if not os.path.isabs(upload_dir):
                upload_dir = os.path.join(current_app.root_path, upload_dir)
            os.makedirs(upload_dir, exist_ok=True)

            # If value is a URL, download
            if s.lower().startswith('http://') or s.lower().startswith('https://'):
                try:
                    parsed = urllib.parse.urlparse(s)
                    basename = os.path.basename(parsed.path) or f'image_{uuid.uuid4().hex}'
                    safe_name = f"{uuid.uuid4().hex}_{basename}"
                    dest = os.path.join(upload_dir, safe_name)
                    urllib.request.urlretrieve(s, dest)
                    return safe_name
                except Exception:
                    # fallback: store the original URL so templates can try to load it
                    return s

            # If it's a local path
            # Try as absolute first
            if os.path.isabs(s) and os.path.exists(s):
                try:
                    basename = os.path.basename(s)
                    safe_name = f"{uuid.uuid4().hex}_{basename}"
                    dest = os.path.join(upload_dir, safe_name)
                    shutil.copy2(s, dest)
                    return safe_name
                except Exception:
                    return None

            # Try relative paths from app root, static/uploads, and project uploads
            candidates = [
                os.path.join(current_app.root_path, s),
                os.path.join(current_app.root_path, 'static', s),
                os.path.join(current_app.root_path, 'static', 'uploads', s),
                os.path.join(current_app.root_path, 'uploads', s),
            ]
            for c in candidates:
                if os.path.exists(c):
                    try:
                        basename = os.path.basename(c)
                        # If already in upload_dir, keep basename
                        if os.path.abspath(c).startswith(os.path.abspath(upload_dir)):
                            return basename
                        safe_name = f"{uuid.uuid4().hex}_{basename}"
                        dest = os.path.join(upload_dir, safe_name)
                        shutil.copy2(c, dest)
                        return safe_name
                    except Exception:
                        continue

            # If nothing matched, return the original value (could be a basename
            # that maps to a static file already present under static/)
            return s

        s.picture = process_picture(pic_val)

        # created_at: let SQLAlchemy default if missing
        if 'created_at' in row and not pd.isna(row['created_at']):
            try:
                s.created_at = pd.to_datetime(row['created_at']).to_pydatetime()
            except Exception:
                pass

        db.session.add(s)
        processed += 1

    if commit:
        db.session.commit()
    return processed


def export_to_excel(path):
    """
    Export all students to an .xlsx at `path`. Returns number of rows exported.
    """
    students = Student.query.order_by(Student.id).all()
    rows = []
    for s in students:
        rows.append({
            'id': s.id,
            'name': s.name,
            'course': s.course,
            'hobbies': s.hobbies,
            'languages': s.languages,
            'motto': s.motto,
            'career_interests': s.career_interests,
            'reason': s.reason,
            'picture': s.picture,
            'created_at': s.created_at,
        })
    df = pd.DataFrame(rows)
    df.to_excel(path, index=False, engine='openpyxl')
    return len(rows)