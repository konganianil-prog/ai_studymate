import os
import re
from werkzeug.utils import secure_filename
from flask import jsonify, request

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename: str) -> bool:
    """Checks if the file extension is supported."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_filename(filename: str) -> str:
    """Creates a sanitized, safe filename."""
    name = secure_filename(filename)
    # Ensure fallback if empty
    if not name:
        name = "uploaded_document"
    return name

def api_response(success=True, data=None, message="", status_code=200):
    """Standardized JSON API response."""
    payload = {
        "success": success,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(payload), status_code

def format_file_size(size_bytes: int) -> str:
    """Formats bytes to readable KB/MB string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
