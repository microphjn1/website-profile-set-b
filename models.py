from datetime import datetime
from ext import db

class Student(db.Model):
    __tablename__ = 'Student'  # or 'Student', just keep it consistent

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(100), nullable=True)
    hobbies = db.Column(db.Text, nullable=True)
    languages = db.Column(db.String(200), nullable=True)
    motto = db.Column(db.Text, nullable=True)
    career_interests = db.Column(db.String(200), nullable=True)
    reason = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'course': self.course,
            'hobbies': self.hobbies,
            'languages': self.languages,
            'motto': self.motto,
            'career_interests': self.career_interests,
            'reason': self.reason,
            'picture': self.picture,
        }
