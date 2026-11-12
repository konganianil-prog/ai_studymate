from datetime import datetime
from backend.extensions import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    
    title = db.Column(db.String(200), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    question_count = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='quizzes')
    subject = db.relationship('Subject', back_populates='quizzes')
    unit = db.relationship('Unit', back_populates='quizzes')
    questions = db.relationship('QuizQuestion', back_populates='quiz', cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', back_populates='quiz', cascade='all, delete-orphan')

    def to_dict(self, include_questions=False, hide_answers=False):
        data = {
            'id': self.id,
            'title': self.title,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'question_count': len(self.questions),
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': self.unit.title if self.unit else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }
        if include_questions:
            data['questions'] = [q.to_dict(hide_answer=hide_answers) for q in self.questions]
        return data

    def __repr__(self):
        return f'<Quiz {self.id}: {self.title}>'


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_option = db.Column(db.String(2), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=True)

    # Relationships
    quiz = db.relationship('Quiz', back_populates='questions')

    def to_dict(self, hide_answer=False):
        data = {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
        }
        if not hide_answer:
            data['correct_option'] = self.correct_option
            data['explanation'] = self.explanation or ''
        return data

    def __repr__(self):
        return f'<QuizQuestion {self.id}>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    details_json = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    quiz = db.relationship('Quiz', back_populates='attempts')
    user = db.relationship('User', back_populates='quiz_attempts')

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'quiz_title': self.quiz.title if self.quiz else 'Quiz',
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': round(self.percentage, 1),
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M') if self.completed_at else ''
        }


class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    
    topic = db.Column(db.String(150), nullable=True)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    is_known = db.Column(db.Boolean, default=False)
    review_count = db.Column(db.Integer, default=0)
    last_reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='flashcards')
    subject = db.relationship('Subject', back_populates='flashcards')
    unit = db.relationship('Unit', back_populates='flashcards')

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic or 'General',
            'front': self.front,
            'back': self.back,
            'is_known': self.is_known,
            'review_count': self.review_count,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': self.unit.title if self.unit else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }

    def __repr__(self):
        return f'<Flashcard {self.id}>'
