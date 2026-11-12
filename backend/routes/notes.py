import re
from io import BytesIO
from flask import Blueprint, request, send_file
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.note import StudyNote
from backend.models.subject import Subject, Unit
from backend.services.pdf_service import PDFService
from backend.utils.helpers import api_response

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('', methods=['GET'])
@login_required
def list_notes():
    query = request.args.get('q', '').strip()
    subject_id = request.args.get('subject_id')

    q_filter = StudyNote.query.filter_by(user_id=current_user.id)
    if subject_id and subject_id.isdigit():
        q_filter = q_filter.filter_by(subject_id=int(subject_id))
    if query:
        pattern = f"%{query}%"
        q_filter = q_filter.filter(
            (StudyNote.title.ilike(pattern)) |
            (StudyNote.content.ilike(pattern)) |
            (StudyNote.tags.ilike(pattern))
        )

    notes = q_filter.order_by(StudyNote.is_pinned.desc(), StudyNote.created_at.desc()).all()
    return api_response(True, data=[n.to_dict() for n in notes])

@notes_bp.route('', methods=['POST'])
@login_required
def create_note():
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    tags = data.get('tags', '').strip()
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    language = data.get('language', 'en')

    if not title or not content:
        return api_response(False, message="Title and Content are required", status_code=400)

    subject_id = int(subject_id) if subject_id and str(subject_id).isdigit() else None
    unit_id = int(unit_id) if unit_id and str(unit_id).isdigit() else None

    note = StudyNote(
        user_id=current_user.id,
        subject_id=subject_id,
        unit_id=unit_id,
        title=title,
        content=content,
        tags=tags,
        language=language
    )
    db.session.add(note)
    db.session.commit()
    return api_response(True, data=note.to_dict(), message="Note created successfully!")

@notes_bp.route('/<int:note_id>', methods=['GET'])
@login_required
def get_note(note_id):
    note = StudyNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    return api_response(True, data=note.to_dict())

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = StudyNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}

    if 'title' in data:
        note.title = data['title'].strip()
    if 'content' in data:
        note.content = data['content'].strip()
    if 'tags' in data:
        note.tags = data['tags'].strip()
    if 'is_pinned' in data:
        note.is_pinned = bool(data['is_pinned'])
    if 'subject_id' in data:
        note.subject_id = int(data['subject_id']) if data['subject_id'] else None
    if 'unit_id' in data:
        note.unit_id = int(data['unit_id']) if data['unit_id'] else None

    db.session.commit()
    return api_response(True, data=note.to_dict(), message="Note updated successfully")

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = StudyNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return api_response(True, message="Note deleted")

@notes_bp.route('/<int:note_id>/pdf', methods=['GET'])
@login_required
def export_note_pdf(note_id):
    note = StudyNote.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()

    subject_name = note.subject.name if note.subject else "General"
    unit_title = note.unit.title if note.unit else "General Unit"

    # Extract marks from title if pattern exists
    m = re.search(r'(\d+)\s*M', note.title, re.IGNORECASE)
    marks = int(m.group(1)) if m else 5

    pdf_bytes = PDFService.generate_note_pdf(
        title=note.title,
        content=note.content,
        subject=subject_name,
        unit=unit_title,
        marks=marks,
        language_mode=note.language or 'en'
    )

    safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', note.title)[:30]
    filename = f"{safe_title}_StudyNotes.pdf"

    return send_file(
        BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
