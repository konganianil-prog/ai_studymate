import json
from flask import Blueprint, request, current_app
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.answer import GeneratedAnswer
from backend.models.note import StudyNote
from backend.models.document import Document, ExtractedQuestion
from backend.models.subject import Subject, Unit
from backend.services.ai_service import AIService
from backend.utils.helpers import api_response

answers_bp = Blueprint('answers', __name__, url_prefix='/api/answers')

@answers_bp.route('', methods=['GET'])
@login_required
def list_answers():
    answers = GeneratedAnswer.query.filter_by(user_id=current_user.id).order_by(GeneratedAnswer.created_at.desc()).all()
    return api_response(True, data=[a.to_dict() for a in answers])

@answers_bp.route('/generate', methods=['POST'])
@login_required
def generate_answer():
    data = request.get_json() or {}
    question_text = data.get('question_text', '').strip()
    marks = int(data.get('marks', 5))
    language_mode = data.get('language_mode', 'en').strip()
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    document_id = data.get('document_id')
    extracted_question_id = data.get('extracted_question_id')

    if not question_text:
        return api_response(False, message="Question text is required.", status_code=400)

    if marks not in (2, 5, 7, 10):
        marks = 5

    subject_id = int(subject_id) if subject_id and str(subject_id).isdigit() else None
    unit_id = int(unit_id) if unit_id and str(unit_id).isdigit() else None
    document_id = int(document_id) if document_id and str(document_id).isdigit() else None
    extracted_question_id = int(extracted_question_id) if extracted_question_id and str(extracted_question_id).isdigit() else None

    # Retrieve context from DB if available
    subject_name = None
    unit_title = None
    context_text = None

    if subject_id:
        sub = Subject.query.get(subject_id)
        if sub:
            subject_name = sub.name

    if unit_id:
        u = Unit.query.get(unit_id)
        if u:
            unit_title = u.title

    if document_id:
        doc = Document.query.filter_by(id=document_id, user_id=current_user.id).first()
        if doc and doc.extracted_text:
            context_text = doc.extracted_text

    # Initialize AI service
    ai_service = AIService(
        api_key=current_app.config.get('GEMINI_API_KEY'),
        model_name=current_app.config.get('GEMINI_MODEL')
    )

    try:
        result = ai_service.generate_answer(
            question_text=question_text,
            marks=marks,
            language_mode=language_mode,
            subject_name=subject_name,
            unit_title=unit_title,
            context_text=context_text
        )

        # Store generated answer in DB
        ans = GeneratedAnswer(
            user_id=current_user.id,
            document_id=document_id,
            extracted_question_id=extracted_question_id,
            subject_id=subject_id,
            unit_id=unit_id,
            question_text=question_text,
            marks=marks,
            language_mode=language_mode,
            raw_answer=result['raw_answer'],
            telugu_explanation=result.get('telugu_explanation', ''),
            diagram_suggestion=result.get('diagram_suggestion', ''),
            key_points_json=json.dumps(result.get('key_points', []))
        )
        db.session.add(ans)
        db.session.commit()

        response_data = ans.to_dict()
        response_data['is_ai_live'] = result.get('is_ai_live', False)
        return api_response(True, data=response_data, message=f"{marks}-mark answer generated successfully!")

    except Exception as e:
        db.session.rollback()
        return api_response(False, message=f"Failed to generate answer: {str(e)}", status_code=500)

@answers_bp.route('/<int:ans_id>', methods=['GET'])
@login_required
def get_answer(ans_id):
    ans = GeneratedAnswer.query.filter_by(id=ans_id, user_id=current_user.id).first_or_404()
    return api_response(True, data=ans.to_dict())

@answers_bp.route('/<int:ans_id>', methods=['PUT'])
@login_required
def update_answer(ans_id):
    ans = GeneratedAnswer.query.filter_by(id=ans_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    
    if 'raw_answer' in data:
        ans.raw_answer = data['raw_answer'].strip()
    if 'telugu_explanation' in data:
        ans.telugu_explanation = data['telugu_explanation'].strip()
    if 'diagram_suggestion' in data:
        ans.diagram_suggestion = data['diagram_suggestion'].strip()

    db.session.commit()
    return api_response(True, data=ans.to_dict(), message="Answer updated successfully")

@answers_bp.route('/<int:ans_id>', methods=['DELETE'])
@login_required
def delete_answer(ans_id):
    ans = GeneratedAnswer.query.filter_by(id=ans_id, user_id=current_user.id).first_or_404()
    db.session.delete(ans)
    db.session.commit()
    return api_response(True, message="Answer deleted")

@answers_bp.route('/<int:ans_id>/save-note', methods=['POST'])
@login_required
def save_answer_as_note(ans_id):
    ans = GeneratedAnswer.query.filter_by(id=ans_id, user_id=current_user.id).first_or_404()
    
    title = f"{ans.marks}M: {ans.question_text[:50]}"
    tags = f"{ans.marks} Marks, {ans.subject.name if ans.subject else 'Study Material'}"
    
    note = StudyNote(
        user_id=current_user.id,
        subject_id=ans.subject_id,
        unit_id=ans.unit_id,
        title=title,
        content=ans.raw_answer,
        tags=tags,
        language=ans.language_mode
    )
    db.session.add(note)
    db.session.commit()

    return api_response(True, data=note.to_dict(), message="Saved directly to Study Notes!")
