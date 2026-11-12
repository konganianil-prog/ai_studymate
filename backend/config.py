import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory is the project root (one level up from backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ai-studymate-super-secret-key-change-in-production')
    
    # Database config: default to SQLite in the project root
    DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'study_mate.db'}")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 20 * 1024 * 1024))  # 20 MB default
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    GENERATED_FOLDER = os.getenv('GENERATED_FOLDER', str(BASE_DIR / 'generated'))
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # AI configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '').strip()
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # App Mode
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PORT = int(os.getenv('PORT', 5000))
