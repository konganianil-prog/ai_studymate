from datetime import datetime
from backend.extensions import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # pdf, docx, txt
    file_size = db.Column(db.Integer, nullable=False)      # bytes
    extracted_text = db.Column(db.Text, nullable=True)
    page_count = db.Column(db.Integer, default=1)
    ocr_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='documents')
    subject = db.relationship('Subject', back_populates='documents')
    unit = db.relationship('Unit', back_populates='documents')
    extracted_questions = db.relationship('ExtractedQuestion', back_populates='document', cascade='all, delete-orphan')
    answers = db.relationship('GeneratedAnswer', back_populates='document')

    def to_dict(self, include_text=False):
        data = {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'file_size_formatted': f"{self.file_size / 1024:.1f} KB" if self.file_size < 1024*1024 else f"{self.file_size / (1024*1024):.2f} MB",
            'page_count': self.page_count,
            'ocr_used': self.ocr_used,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': self.unit.title if self.unit else None,
            'questions_count': len(self.extracted_questions),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }
        if include_text:
            data['extracted_text'] = self.extracted_text
        return data

    def __repr__(self):
        return f'<Document {self.original_filename}>'


class ExtractedQuestion(db.Model):
    __tablename__ = 'extracted_questions'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_number = db.Column(db.String(50), nullable=True)
    suggested_marks = db.Column(db.Integer, default=5)
    unit_context = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    document = db.relationship('Document', back_populates='extracted_questions')
    generated_answers = db.relationship('GeneratedAnswer', back_populates='extracted_question')

    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'question_text': self.question_text,
            'question_number': self.question_number or '',
            'suggested_marks': self.suggested_marks or 5,
            'unit_context': self.unit_context or ''
        }

    def __repr__(self):
        return f'<ExtractedQuestion {self.id}: {self.question_text[:30]}...>'
