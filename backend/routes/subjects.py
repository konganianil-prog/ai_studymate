from flask import Blueprint, request
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.subject import Subject, Unit
from backend.utils.helpers import api_response

subjects_bp = Blueprint('subjects', __name__, url_prefix='/api/subjects')

@subjects_bp.route('', methods=['GET'])
@login_required
def list_subjects():
    subjects = Subject.query.filter(
        (Subject.user_id == current_user.id) | (Subject.user_id == None)
    ).all()
    return api_response(True, data=[s.to_dict() for s in subjects])

@subjects_bp.route('', methods=['POST'])
@login_required
def create_subject():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    code = data.get('code', '').strip()
    description = data.get('description', '').strip()
    icon = data.get('icon', 'bi-book').strip()

    if not name:
        return api_response(False, message="Subject name is required", status_code=400)

    subject = Subject(
        name=name,
        code=code,
        description=description,
        icon=icon or 'bi-book',
        user_id=current_user.id
    )
    db.session.add(subject)
    db.session.commit()
    return api_response(True, data=subject.to_dict(), message="Subject created successfully!")

@subjects_bp.route('/<int:subject_id>/units', methods=['GET'])
@login_required
def list_units(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return api_response(True, data=[u.to_dict() for u in subject.units])

@subjects_bp.route('/<int:subject_id>/units', methods=['POST'])
@login_required
def create_unit(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    unit_number = int(data.get('unit_number', len(subject.units) + 1))
    description = data.get('description', '').strip()

    if not title:
        return api_response(False, message="Unit title is required", status_code=400)

    unit = Unit(
        subject_id=subject.id,
        unit_number=unit_number,
        title=title,
        description=description
    )
    db.session.add(unit)
    db.session.commit()
    return api_response(True, data=unit.to_dict(), message="Unit added successfully!")

@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        return api_response(False, message="Cannot delete system default subjects", status_code=403)
    
    db.session.delete(subject)
    db.session.commit()
    return api_response(True, message="Subject deleted successfully")
