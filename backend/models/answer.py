from datetime import datetime
from backend.extensions import db

class GeneratedAnswer(db.Model):
    __tablename__ = 'generated_answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='SET NULL'), nullable=True)
    extracted_question_id = db.Column(db.Integer, db.ForeignKey('extracted_questions.id', ondelete='SET NULL'), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='SET NULL'), nullable=True)

    question_text = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, default=5)               # 2, 5, 7, 10
    language_mode = db.Column(db.String(20), default='en') # 'en', 'te', 'en_te'
    
    # Store complete structured response
    raw_answer = db.Column(db.Text, nullable=False)
    telugu_explanation = db.Column(db.Text, nullable=True)
    diagram_suggestion = db.Column(db.Text, nullable=True)
    key_points_json = db.Column(db.Text, nullable=True)     # JSON string of bullet points
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='answers')
    document = db.relationship('Document', back_populates='answers')
    extracted_question = db.relationship('ExtractedQuestion', back_populates='generated_answers')
    subject = db.relationship('Subject', back_populates='answers')
    unit = db.relationship('Unit', back_populates='answers')

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'marks': self.marks,
            'language_mode': self.language_mode,
            'raw_answer': self.raw_answer,
            'telugu_explanation': self.telugu_explanation or '',
            'diagram_suggestion': self.diagram_suggestion or '',
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': self.unit.title if self.unit else None,
            'document_id': self.document_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }

    def __repr__(self):
        return f'<GeneratedAnswer {self.id}: {self.marks} marks>'


class GeneratedVisual(db.Model):
    __tablename__ = 'generated_visuals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    visual_type = db.Column(db.String(50), default='flowchart')  # flowchart, mindmap, diagram, image
    prompt = db.Column(db.Text, nullable=True)
    diagram_code = db.Column(db.Text, nullable=True)              # Mermaid.js or SVG markup
    image_url = db.Column(db.String(500), nullable=True)         # Relative file path or placeholder
    explanation = db.Column(db.Text, nullable=True)
    steps_json = db.Column(db.Text, nullable=True)               # JSON array of steps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='visuals')

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'visual_type': self.visual_type,
            'diagram_code': self.diagram_code or '',
            'image_url': self.image_url or '',
            'explanation': self.explanation or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }

    def __repr__(self):
        return f'<GeneratedVisual {self.id}: {self.topic}>'
