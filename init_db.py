from flask import Flask
from ext import db
from models import Student
import os

# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create instance directory if it doesn't exist
os.makedirs('instance', exist_ok=True)

# Student data from all templates
students_data = [
    {
        'name': 'NUEVO, ROSALYN',
        'picture': 'uploads/NUEVO.jpg',
        'course': 'BSIT',
        'career_interests': 'Software Engineer',
        'hobbies': 'Coding, Problem Solving',
        'languages': 'Python, Java',
        'motto': 'Code with passion',
        'reason': 'Passionate about software development'
    },
    {
        'name': 'Ramos, Sean Axl G.',
        'picture': 'uploads/Silver.png',
        'course': 'BSIT',
        'career_interests': 'Software Engineer',
        'hobbies': 'Programming, Gaming',
        'languages': 'Python, JavaScript',
        'motto': 'Innovation through code',
        'reason': 'Love creating software solutions'
    },
    {
        'name': 'Olveda, Angeline',
        'picture': 'uploads/Olveda.jpg',
        'course': 'BSIT',
        'career_interests': 'Database Administrator',
        'hobbies': 'Database Design',
        'languages': 'SQL, Python',
        'motto': 'Data is the new gold',
        'reason': 'Passionate about data management'
    },
    {
        'name': 'Provido, Rasheed Rai',
        'picture': 'uploads/provido.jpg',
        'course': 'BSIT',
        'career_interests': 'Cybersecurity Engineer',
        'hobbies': 'Security Research',
        'languages': 'Python, Shell Scripting',
        'motto': 'Security first',
        'reason': 'Dedicated to cybersecurity'
    },
    {
        'name': 'PELAEZ, SANDARAH N.',
        'picture': 'uploads/PELAEZ.jpg',
        'course': 'BSIT',
        'career_interests': 'UI/UX Designer',
        'hobbies': 'Design, Art',
        'languages': 'HTML, CSS, JavaScript',
        'motto': 'Design with purpose',
        'reason': 'Passionate about user experience'
    },
    {
        'name': 'Gubala, Jane Mariel',
        'picture': 'uploads/Gubala.jpg',
        'course': 'BSIT',
        'career_interests': 'UI/UX Designer',
        'hobbies': 'Web Design',
        'languages': 'HTML, CSS',
        'motto': 'Create beautiful experiences',
        'reason': 'Love making beautiful interfaces'
    },
    {
        'name': 'ZAMORA, KENNETH',
        'picture': 'uploads/ZAMORA.jpg',
        'course': 'BSIT',
        'career_interests': 'Mobile Developer',
        'hobbies': 'Mobile App Development',
        'languages': 'Java, Kotlin',
        'motto': 'Mobile first',
        'reason': 'Passionate about mobile technology'
    },
    {
        'name': 'QUIRANTE, LANCE MICHAEL D.',
        'picture': 'uploads/QUIRANTE.jpg',
        'course': 'BSIT',
        'career_interests': 'Business Analyst',
        'hobbies': 'Business Analysis',
        'languages': 'SQL, Python',
        'motto': 'Bridge business and technology',
        'reason': 'Interest in business solutions'
    },
    {
        'name': 'Legarde, Xyrus James D.',
        'picture': 'uploads/Legarde.jpg',
        'course': 'BSCS',
        'career_interests': 'DevOps Engineer',
        'hobbies': 'System Administration',
        'languages': 'Python, Shell, Docker',
        'motto': 'Automate everything',
        'reason': 'Passionate about DevOps'
    },
    {
        'name': 'Abuan, Allen James G.',
        'picture': 'uploads/Abuan.jpg',
        'course': 'BSIT',
        'career_interests': 'Data Analyst',
        'hobbies': 'Data Analysis',
        'languages': 'Python, R, SQL',
        'motto': 'Data drives decisions',
        'reason': 'Love working with data'
    }
]

def init_db():
    # Create the database
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(app.static_folder, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Add all students
        for student_data in students_data:
            student = Student(
                name=student_data['name'],
                picture=student_data['picture'],
                course=student_data['course'],
                career_interests=student_data['career_interests'],
                hobbies=student_data['hobbies'],
                languages=student_data['languages'],
                motto=student_data['motto'],
                reason=student_data['reason']
            )
            db.session.add(student)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Database initialized successfully!")
            print(f"Added {len(students_data)} students to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_db()