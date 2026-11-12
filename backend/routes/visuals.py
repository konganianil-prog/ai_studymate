import os
import json
from flask import Blueprint, request, current_app, send_from_directory
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.answer import GeneratedVisual
from backend.services.ai_service import AIService
from backend.services.image_service import ImageService
from backend.utils.helpers import api_response

visuals_bp = Blueprint('visuals', __name__)

@visuals_bp.route('/generated/<path:filename>')
def serve_generated_file(filename):
    """Serves generated diagrams and educational images."""
    return send_from_directory(current_app.config['GENERATED_FOLDER'], filename)

@visuals_bp.route('/api/visuals', methods=['GET'])
@login_required
def list_visuals():
    visuals = GeneratedVisual.query.filter_by(user_id=current_user.id).order_by(GeneratedVisual.created_at.desc()).all()
    return api_response(True, data=[v.to_dict() for v in visuals])

@visuals_bp.route('/api/visuals/generate', methods=['POST'])
@login_required
def generate_visual():
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()
    visual_type = data.get('visual_type', 'flowchart').strip()

    if not topic:
        return api_response(False, message="Topic is required.", status_code=400)

    ai_service = AIService(
        api_key=current_app.config.get('GEMINI_API_KEY'),
        model_name=current_app.config.get('GEMINI_MODEL')
    )

    try:
        # Generate visual concept content (flowchart / mindmap / steps / explanation)
        concept = ai_service.generate_visual_concept(topic)

        # Generate educational SVG illustration
        svg_url = ImageService.generate_educational_svg(
            topic, current_app.config['GENERATED_FOLDER']
        )

        diagram_code = concept.get('mermaid_flowchart') if visual_type == 'flowchart' else concept.get('mermaid_mindmap')

        # Save to database
        visual_rec = GeneratedVisual(
            user_id=current_user.id,
            topic=topic,
            visual_type=visual_type,
            prompt=f"Educational visual for {topic}",
            diagram_code=diagram_code,
            image_url=svg_url,
            explanation=concept.get('explanation', ''),
            steps_json=json.dumps(concept.get('steps', []))
        )
        db.session.add(visual_rec)
        db.session.commit()

        res_data = visual_rec.to_dict()
        res_data['key_points'] = concept.get('key_points', [])
        res_data['steps'] = concept.get('steps', [])
        res_data['real_world_example'] = concept.get('real_world_example', '')
        res_data['mermaid_flowchart'] = concept.get('mermaid_flowchart', '')
        res_data['mermaid_mindmap'] = concept.get('mermaid_mindmap', '')
        res_data['is_ai_live'] = concept.get('is_ai_live', False)

        return api_response(True, data=res_data, message=f"Visual learning map for '{topic}' generated successfully!")

    except Exception as e:
        db.session.rollback()
        return api_response(False, message=f"Failed to generate visual: {str(e)}", status_code=500)

@visuals_bp.route('/api/visuals/<int:vid>', methods=['GET'])
@login_required
def get_visual(vid):
    v = GeneratedVisual.query.filter_by(id=vid, user_id=current_user.id).first_or_404()
    data = v.to_dict()
    data['steps'] = json.loads(v.steps_json) if v.steps_json else []
    return api_response(True, data=data)

@visuals_bp.route('/api/visuals/<int:vid>', methods=['DELETE'])
@login_required
def delete_visual(vid):
    v = GeneratedVisual.query.filter_by(id=vid, user_id=current_user.id).first_or_404()
    db.session.delete(v)
    db.session.commit()
    return api_response(True, message="Visual deleted")
