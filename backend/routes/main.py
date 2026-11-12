from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.document import Document, ExtractedQuestion
from backend.models.answer import GeneratedAnswer, GeneratedVisual
from backend.models.note import StudyNote
from backend.models.quiz import Quiz, QuizAttempt, Flashcard
from backend.models.subject import Subject
from backend.utils.helpers import api_response

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Gather statistics for current user
    user_id = current_user.id
    total_docs = Document.query.filter_by(user_id=user_id).count()
    total_answers = GeneratedAnswer.query.filter_by(user_id=user_id).count()
    total_notes = StudyNote.query.filter_by(user_id=user_id).count()
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    total_quizzes = len(quiz_attempts)
    avg_score = round(sum([a.percentage for a in quiz_attempts]) / total_quizzes, 1) if total_quizzes > 0 else 0
    total_flashcards = Flashcard.query.filter_by(user_id=user_id).count()
    
    # Recent activity
    recent_answers = GeneratedAnswer.query.filter_by(user_id=user_id).order_by(GeneratedAnswer.created_at.desc()).limit(5).all()
    recent_docs = Document.query.filter_by(user_id=user_id).order_by(Document.created_at.desc()).limit(5).all()
    recent_attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()

    subjects = Subject.query.filter((Subject.user_id == user_id) | (Subject.user_id == None)).all()

    return render_template('dashboard.html',
                           total_docs=total_docs,
                           total_answers=total_answers,
                           total_notes=total_notes,
                           total_quizzes=total_quizzes,
                           avg_score=avg_score,
                           total_flashcards=total_flashcards,
                           recent_answers=recent_answers,
                           recent_docs=recent_docs,
                           recent_attempts=recent_attempts,
                           subjects=subjects)

@main_bp.route('/upload')
@login_required
def upload_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    return render_template('upload.html', subjects=subjects)

@main_bp.route('/answers')
@login_required
def answers_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.created_at.desc()).all()
    return render_template('answers.html', subjects=subjects, documents=documents)

@main_bp.route('/visualizer')
@login_required
def visualizer_page():
    return render_template('visualizer.html')

@main_bp.route('/3d-lab')
@login_required
def three_d_lab_page():
    return render_template('3d-lab.html')

@main_bp.route('/quiz')
@login_required
def quiz_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    documents = Document.query.filter_by(user_id=current_user.id).all()
    return render_template('quiz.html', subjects=subjects, documents=documents)

@main_bp.route('/flashcards')
@login_required
def flashcards_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    return render_template('flashcards.html', subjects=subjects)

@main_bp.route('/notes')
@login_required
def notes_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    return render_template('notes.html', subjects=subjects)

@main_bp.route('/subjects')
@login_required
def subjects_page():
    subjects = Subject.query.filter((Subject.user_id == current_user.id) | (Subject.user_id == None)).all()
    return render_template('subjects.html', subjects=subjects)

@main_bp.route('/api/search')
@login_required
def global_search():
    query = request.args.get('q', '').strip()
    if not query:
        return api_response(True, data={'documents': [], 'questions': [], 'answers': [], 'notes': []})

    user_id = current_user.id
    pattern = f"%{query}%"

    docs = Document.query.filter(
        Document.user_id == user_id,
        (Document.original_filename.ilike(pattern) | Document.extracted_text.ilike(pattern))
    ).limit(5).all()

    questions = ExtractedQuestion.query.join(Document).filter(
        Document.user_id == user_id,
        ExtractedQuestion.question_text.ilike(pattern)
    ).limit(8).all()

    answers = GeneratedAnswer.query.filter(
        GeneratedAnswer.user_id == user_id,
        (GeneratedAnswer.question_text.ilike(pattern) | GeneratedAnswer.raw_answer.ilike(pattern))
    ).limit(5).all()

    notes = StudyNote.query.filter(
        StudyNote.user_id == user_id,
        (StudyNote.title.ilike(pattern) | StudyNote.content.ilike(pattern) | StudyNote.tags.ilike(pattern))
    ).limit(5).all()

    return api_response(True, data={
        'documents': [d.to_dict() for d in docs],
        'questions': [q.to_dict() for q in questions],
        'answers': [a.to_dict() for a in answers],
        'notes': [n.to_dict() for n in notes]
    })

@main_bp.route('/api/dashboard/stats')
@login_required
def dashboard_stats():
    user_id = current_user.id
    total_docs = Document.query.filter_by(user_id=user_id).count()
    total_answers = GeneratedAnswer.query.filter_by(user_id=user_id).count()
    total_notes = StudyNote.query.filter_by(user_id=user_id).count()
    quiz_attempts = QuizAttempt.query.filter_by(user_id=user_id).all()
    total_quizzes = len(quiz_attempts)
    avg_score = round(sum([a.percentage for a in quiz_attempts]) / total_quizzes, 1) if total_quizzes > 0 else 0
    total_flashcards = Flashcard.query.filter_by(user_id=user_id).count()

    # Score breakdown for chart
    attempts_history = [
        {"title": a.quiz.title if a.quiz else f"Quiz #{a.id}", "score": a.percentage, "date": a.completed_at.strftime('%m/%d')}
        for a in QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.completed_at.asc()).limit(7).all()
    ]

    return api_response(True, data={
        'total_docs': total_docs,
        'total_answers': total_answers,
        'total_notes': total_notes,
        'total_quizzes': total_quizzes,
        'avg_score': avg_score,
        'total_flashcards': total_flashcards,
        'attempts_history': attempts_history
    })
