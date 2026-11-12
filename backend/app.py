import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from backend.config import Config, BASE_DIR
from backend.extensions import db, login_manager
from backend.models.user import User
from backend.models import seed_default_subjects
from backend.routes import (
    auth_bp,
    main_bp,
    documents_bp,
    answers_bp,
    visuals_bp,
    quizzes_bp,
    notes_bp,
    subjects_bp
)

def create_app(config_class=Config):
    # Determine template and static folders
    template_dir = BASE_DIR / 'frontend' / 'templates'
    static_dir = BASE_DIR / 'frontend' / 'static'
    
    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir)
    )
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(visuals_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(subjects_bp)

    # Context processors
    @app.context_processor
    def inject_global_vars():
        gemini_configured = bool(app.config.get('GEMINI_API_KEY'))
        return {
            'gemini_configured': gemini_configured,
            'app_name': 'AI STUDY MATE'
        }

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Resource not found', 'data': {}}), 404
        return render_template('index.html', error_message="Page not found (404)"), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        max_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        msg = f"File is too large. Maximum allowed size is {max_mb:.0f} MB."
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': msg, 'data': {}}), 413
        return render_template('upload.html', error_message=msg), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Internal server error occurred', 'data': {}}), 500
        return render_template('index.html', error_message="Internal server error (500)"), 500

    # Initialize database tables and seed default subjects
    with app.app_context():
        db.create_all()
        seed_default_subjects()

    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)
    print(f"Starting AI STUDY MATE on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=debug)
