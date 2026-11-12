from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = db.relationship('Document', back_populates='user', cascade='all, delete-orphan')
    answers = db.relationship('GeneratedAnswer', back_populates='user', cascade='all, delete-orphan')
    notes = db.relationship('StudyNote', back_populates='user', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', back_populates='user', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', back_populates='user', cascade='all, delete-orphan')
    flashcards = db.relationship('Flashcard', back_populates='user', cascade='all, delete-orphan')
    visuals = db.relationship('GeneratedVisual', back_populates='user', cascade='all, delete-orphan')
    subjects = db.relationship('Subject', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name or self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
