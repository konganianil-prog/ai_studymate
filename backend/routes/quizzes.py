import json
from datetime import datetime
from flask import Blueprint, request
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.quiz import Quiz, QuizQuestion, QuizAttempt, Flashcard
from backend.models.document import Document
from backend.services.quiz_service import QuizService
from backend.utils.helpers import api_response

quizzes_bp = Blueprint('quizzes', __name__, url_prefix='/api')

@quizzes_bp.route('/quizzes', methods=['GET'])
@login_required
def list_quizzes():
    quizzes = Quiz.query.filter_by(user_id=current_user.id).order_by(Quiz.created_at.desc()).all()
    return api_response(True, data=[q.to_dict(include_questions=True, hide_answers=False) for q in quizzes])

@quizzes_bp.route('/quizzes/generate', methods=['POST'])
@login_required
def generate_quiz():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    count = int(data.get('count', 5))
    difficulty = data.get('difficulty', 'medium').lower()
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    document_id = data.get('document_id')

    if not topic and not document_id:
        return api_response(False, message="Please provide a topic or select a document", status_code=400)

    context_text = None
    if document_id:
        doc = Document.query.filter_by(id=document_id, user_id=current_user.id).first()
        if doc and doc.extracted_text:
            context_text = doc.extracted_text
            if not topic:
                topic = doc.original_filename

    quiz_service = QuizService()
    questions_data = quiz_service.generate_quiz(
        topic=topic,
        count=count,
        difficulty=difficulty,
        context_text=context_text
    )

    if not questions_data:
        return api_response(False, message="Could not generate questions for this topic", status_code=500)

    subject_id = int(subject_id) if subject_id and str(subject_id).isdigit() else None
    unit_id = int(unit_id) if unit_id and str(unit_id).isdigit() else None

    # Save to database
    quiz = Quiz(
        user_id=current_user.id,
        subject_id=subject_id,
        unit_id=unit_id,
        title=f"{topic} Quiz ({difficulty.capitalize()})",
        topic=topic,
        difficulty=difficulty,
        question_count=len(questions_data)
    )
    db.session.add(quiz)
    db.session.flush()

    for q in questions_data:
        qq = QuizQuestion(
            quiz_id=quiz.id,
            question_text=q['question_text'],
            option_a=q['option_a'],
            option_b=q['option_b'],
            option_c=q['option_c'],
            option_d=q['option_d'],
            correct_option=q['correct_option'].upper().strip(),
            explanation=q.get('explanation', '')
        )
        db.session.add(qq)

    db.session.commit()
    return api_response(True, data=quiz.to_dict(include_questions=True, hide_answers=False), message="Quiz created successfully!")

@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=current_user.id).first_or_404()
    practice_mode = request.args.get('practice', 'false').lower() == 'true'
    return api_response(True, data=quiz.to_dict(include_questions=True, hide_answers=not practice_mode))

@quizzes_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    user_answers = data.get('answers', {})  # Map: { "question_id": "A" }

    score = 0
    total = len(quiz.questions)
    results = []

    for q in quiz.questions:
        selected = str(user_answers.get(str(q.id), '')).upper().strip()
        is_correct = (selected == q.correct_option)
        if is_correct:
            score += 1
        results.append({
            'question_id': q.id,
            'question_text': q.question_text,
            'selected_option': selected,
            'correct_option': q.correct_option,
            'is_correct': is_correct,
            'explanation': q.explanation
        })

    percentage = round((score / total) * 100, 1) if total > 0 else 0

    # Save attempt
    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=current_user.id,
        score=score,
        total_questions=total,
        percentage=percentage,
        details_json=json.dumps(results)
    )
    db.session.add(attempt)
    db.session.commit()

    return api_response(True, data={
        'attempt_id': attempt.id,
        'score': score,
        'total': total,
        'percentage': percentage,
        'results': results
    }, message=f"Quiz completed! You scored {score}/{total} ({percentage}%).")

@quizzes_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=current_user.id).first_or_404()
    db.session.delete(quiz)
    db.session.commit()
    return api_response(True, message="Quiz deleted")

# Flashcards Endpoints
@quizzes_bp.route('/flashcards', methods=['GET'])
@login_required
def list_flashcards():
    cards = Flashcard.query.filter_by(user_id=current_user.id).order_by(Flashcard.created_at.desc()).all()
    return api_response(True, data=[c.to_dict() for c in cards])

@quizzes_bp.route('/flashcards/generate', methods=['POST'])
@login_required
def generate_flashcards():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    count = int(data.get('count', 6))
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')

    if not topic:
        return api_response(False, message="Topic is required.", status_code=400)

    quiz_service = QuizService()
    cards_data = quiz_service.generate_flashcards(topic=topic, count=count)

    subject_id = int(subject_id) if subject_id and str(subject_id).isdigit() else None
    unit_id = int(unit_id) if unit_id and str(unit_id).isdigit() else None

    created_cards = []
    for c in cards_data:
        fc = Flashcard(
            user_id=current_user.id,
            subject_id=subject_id,
            unit_id=unit_id,
            topic=topic,
            front=c['front'],
            back=c['back']
        )
        db.session.add(fc)
        created_cards.append(fc)

    db.session.commit()
    return api_response(True, data=[c.to_dict() for c in created_cards], message=f"Generated {len(created_cards)} flashcards!")

@quizzes_bp.route('/flashcards/<int:card_id>/review', methods=['POST'])
@login_required
def review_flashcard(card_id):
    card = Flashcard.query.filter_by(id=card_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    card.is_known = bool(data.get('is_known', True))
    card.review_count += 1
    card.last_reviewed_at = datetime.utcnow()
    db.session.commit()
    return api_response(True, data=card.to_dict())

@quizzes_bp.route('/flashcards/<int:card_id>', methods=['DELETE'])
@login_required
def delete_flashcard(card_id):
    card = Flashcard.query.filter_by(id=card_id, user_id=current_user.id).first_or_404()
    db.session.delete(card)
    db.session.commit()
    return api_response(True, message="Flashcard deleted")
