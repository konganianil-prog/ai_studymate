from datetime import datetime
from backend.extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True) # Nullable for default/global subjects
    name = db.Column(db.String(150), nullable=False, index=True)
    code = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), default='bi-book')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='subjects')
    units = db.relationship('Unit', back_populates='subject', cascade='all, delete-orphan', order_by='Unit.unit_number')
    documents = db.relationship('Document', back_populates='subject')
    answers = db.relationship('GeneratedAnswer', back_populates='subject')
    notes = db.relationship('StudyNote', back_populates='subject')
    quizzes = db.relationship('Quiz', back_populates='subject')
    flashcards = db.relationship('Flashcard', back_populates='subject')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code or '',
            'description': self.description or '',
            'icon': self.icon or 'bi-book',
            'units_count': len(self.units) if self.units else 0,
            'is_default': self.user_id is None
        }

    def __repr__(self):
        return f'<Subject {self.name}>'


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    unit_number = db.Column(db.Integer, default=1)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subject = db.relationship('Subject', back_populates='units')
    documents = db.relationship('Document', back_populates='unit')
    answers = db.relationship('GeneratedAnswer', back_populates='unit')
    notes = db.relationship('StudyNote', back_populates='unit')
    quizzes = db.relationship('Quiz', back_populates='unit')
    flashcards = db.relationship('Flashcard', back_populates='unit')

    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'unit_number': self.unit_number,
            'title': self.title,
            'description': self.description or ''
        }

    def __repr__(self):
        return f'<Unit {self.unit_number}: {self.title}>'
