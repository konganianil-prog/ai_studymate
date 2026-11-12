import os
from flask import Blueprint, request, current_app
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.document import Document, ExtractedQuestion
from backend.services.document_service import DocumentService
from backend.utils.helpers import api_response, allowed_file

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@documents_bp.route('', methods=['GET'])
@login_required
def list_documents():
    docs = Document.query.filter_by(user_id=current_user.id).order_by(Document.created_at.desc()).all()
    return api_response(True, data=[d.to_dict() for d in docs])

@documents_bp.route('/upload', methods=['POST'])
@login_required
def upload_document():
    if 'file' not in request.files:
        return api_response(False, message="No file part in the request", status_code=400)

    file = request.files['file']
    if file.filename == '':
        return api_response(False, message="No file selected for upload", status_code=400)

    subject_id = request.form.get('subject_id')
    unit_id = request.form.get('unit_id')
    subject_id = int(subject_id) if subject_id and subject_id.isdigit() else None
    unit_id = int(unit_id) if unit_id and unit_id.isdigit() else None

    try:
        # Save file securely
        saved_name, original_name, file_size, ext = DocumentService.save_uploaded_file(
            file, current_app.config['UPLOAD_FOLDER']
        )
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], saved_name)

        # Extract text & metadata
        extracted_text, page_count, ocr_used = DocumentService.extract_text_and_meta(filepath, ext)

        # Create Document record
        doc = Document(
            user_id=current_user.id,
            subject_id=subject_id,
            unit_id=unit_id,
            filename=saved_name,
            original_filename=original_name,
            file_type=ext,
            file_size=file_size,
            extracted_text=extracted_text,
            page_count=page_count,
            ocr_used=ocr_used
        )
        db.session.add(doc)
        db.session.flush()

        # Extract questions
        parsed_questions = DocumentService.extract_questions(extracted_text)
        created_questions = []
        for q in parsed_questions:
            eq = ExtractedQuestion(
                document_id=doc.id,
                question_text=q['question_text'],
                question_number=q['question_number'],
                suggested_marks=q['suggested_marks'],
                unit_context=q['unit_context']
            )
            db.session.add(eq)
            created_questions.append(eq)

        db.session.commit()

        return api_response(
            True,
            data={
                'document': doc.to_dict(include_text=True),
                'questions': [q.to_dict() for q in created_questions]
            },
            message=f"Successfully processed {original_name}. Found {len(created_questions)} questions."
        )

    except ValueError as ve:
        return api_response(False, message=str(ve), status_code=400)
    except Exception as e:
        db.session.rollback()
        return api_response(False, message=f"Failed to process document: {str(e)}", status_code=500)

@documents_bp.route('/<int:doc_id>', methods=['GET'])
@login_required
def get_document(doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    return api_response(True, data={
        'document': doc.to_dict(include_text=True),
        'questions': [q.to_dict() for q in doc.extracted_questions]
    })

@documents_bp.route('/<int:doc_id>/questions', methods=['GET'])
@login_required
def get_document_questions(doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    return api_response(True, data=[q.to_dict() for q in doc.extracted_questions])

@documents_bp.route('/<int:doc_id>', methods=['DELETE'])
@login_required
def delete_document(doc_id):
    doc = Document.query.filter_by(id=doc_id, user_id=current_user.id).first_or_404()
    
    # Remove physical file if exists
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass

    db.session.delete(doc)
    db.session.commit()
    return api_response(True, message="Document deleted successfully")
