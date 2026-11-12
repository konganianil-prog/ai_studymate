from datetime import datetime
from backend.extensions import db

class StudyNote(db.Model):
    __tablename__ = 'study_notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=True)          # Comma-separated tags
    language = db.Column(db.String(20), default='en')        # 'en', 'te', 'en_te'
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='notes')
    subject = db.relationship('Subject', back_populates='notes')
    unit = db.relationship('Unit', back_populates='notes')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': [t.strip() for t in self.tags.split(',') if t.strip()] if self.tags else [],
            'language': self.language,
            'is_pinned': self.is_pinned,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': self.unit.title if self.unit else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else ''
        }

    def __repr__(self):
        return f'<StudyNote {self.id}: {self.title}>'
