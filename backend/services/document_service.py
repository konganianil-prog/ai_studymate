import os
import re
import uuid
from typing import Tuple, List, Dict, Any
from werkzeug.utils import secure_filename
from backend.utils.helpers import allowed_file, clean_filename

class DocumentService:
    @staticmethod
    def save_uploaded_file(file_storage, upload_folder: str) -> Tuple[str, str, int, str]:
        """
        Saves uploaded file securely.
        Returns: (saved_relative_filename, original_filename, file_size, extension)
        """
        original_filename = clean_filename(file_storage.filename)
        ext = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else ''
        
        if not allowed_file(original_filename):
            raise ValueError(f"Unsupported file type .{ext}. Allowed: PDF, DOCX, TXT")

        unique_prefix = uuid.uuid4().hex[:12]
        safe_name = f"{unique_prefix}_{original_filename}"
        full_path = os.path.join(upload_folder, safe_name)
        
        file_storage.save(full_path)
        file_size = os.path.getsize(full_path)
        
        if file_size == 0:
            if os.path.exists(full_path):
                os.remove(full_path)
            raise ValueError("Uploaded file is empty (0 bytes).")

        return safe_name, original_filename, file_size, ext

    @staticmethod
    def extract_text_and_meta(filepath: str, ext: str) -> Tuple[str, int, bool]:
        """
        Extracts plain text and page count from document.
        Returns: (extracted_text, page_count, ocr_used)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        ext = ext.lower()
        if ext == 'pdf':
            return DocumentService._extract_pdf(filepath)
        elif ext == 'docx':
            return DocumentService._extract_docx(filepath)
        elif ext == 'txt':
            return DocumentService._extract_txt(filepath)
        else:
            raise ValueError(f"Unsupported extension: {ext}")

    @staticmethod
    def _extract_pdf(filepath: str) -> Tuple[str, int, bool]:
        """Extracts text from PDF using PyMuPDF, falling back to pypdf or OCR."""
        text_pages = []
        page_count = 0
        ocr_used = False

        # 1. Try PyMuPDF
        try:
            import pymupdf as fitz
            doc = fitz.open(filepath)
            page_count = len(doc)
            for page in doc:
                t = page.get_text()
                if t:
                    text_pages.append(t.strip())
            doc.close()
        except Exception:
            # 2. Fallback to pypdf
            try:
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                page_count = len(reader.pages)
                for page in reader.pages:
                    t = page.extract_text()
                    if t:
                        text_pages.append(t.strip())
            except Exception as pypdf_err:
                raise ValueError(f"Failed to extract PDF contents: {pypdf_err}")

        extracted_text = "\n\n".join(text_pages).strip()

        # If scanned PDF, try OCR with pytesseract
        if len(extracted_text) < 30 and page_count > 0:
            try:
                import pytesseract
                from PIL import Image
                import pymupdf as fitz
                
                doc = fitz.open(filepath)
                ocr_texts = []
                for i in range(min(5, page_count)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    ocr_result = pytesseract.image_to_string(img)
                    if ocr_result:
                        ocr_texts.append(ocr_result.strip())
                doc.close()
                if ocr_texts:
                    extracted_text = "\n\n".join(ocr_texts).strip()
                    ocr_used = True
            except Exception:
                pass

        if not extracted_text:
            extracted_text = "[No readable text found in this PDF. The document may contain scanned images without OCR.]"

        return extracted_text, max(page_count, 1), ocr_used

    @staticmethod
    def _extract_docx(filepath: str) -> Tuple[str, int, bool]:
        """Extracts text and tables from DOCX files."""
        try:
            from docx import Document as DocxDoc
            doc = DocxDoc(filepath)
            full_text = []

            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text.strip())

            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        full_text.append(" | ".join(row_text))

            text = "\n\n".join(full_text).strip()
            word_count = len(text.split())
            estimated_pages = max(1, (word_count + 399) // 400)
            return text or "[Empty Word document]", estimated_pages, False
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")

    @staticmethod
    def _extract_txt(filepath: str) -> Tuple[str, int, bool]:
        """Reads plain text file with encoding fallback."""
        content = ""
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        line_count = len(content.splitlines())
        estimated_pages = max(1, (line_count + 49) // 50)
        return content.strip(), estimated_pages, False

    @staticmethod
    def extract_questions(text: str) -> List[Dict[str, Any]]:
        """
        Parses text and extracts potential examination questions, their suggested marks,
        and unit contexts.
        """
        if not text:
            return []

        questions = []
        lines = text.split('\n')
        current_unit = "General"

        # Regex for Unit headers
        unit_regex = re.compile(r'^(?:UNIT|MODULE|SECTION|PART)\s*[-:]?\s*([0-9IVXLCDM]+|[A-Z])', re.IGNORECASE)
        
        # Regex patterns for question starters:
        # Matches: Q1., Q1:, Q.1, Q 1., Question 1:, 1., 1), (1), (a), a)
        q_start_regex = re.compile(
            r'^(?:(?:Q|Question)\s*[-.:]?\s*(\d+[a-zA-Z]?)[-.:)]*|(\d{1,3})[.)\]:]|\(([0-9a-zA-Z]+)\))\s+(.+)',
            re.IGNORECASE
        )

        # Regex for marks inside question: [5M], (5 Marks), 10 marks, [10], (2M)
        marks_regex = re.compile(r'\[?\(?(\d{1,2})\s*(?:M|Marks|marks|mark)\)?\]?', re.IGNORECASE)

        def normalize_marks(m_val: int) -> int:
            if m_val <= 3:
                return 2
            elif m_val <= 6:
                return 5
            elif m_val <= 8:
                return 7
            else:
                return 10

        def save_current_question(q_num, q_parts, marks, unit):
            if not q_parts:
                return
            full_q = " ".join(q_parts).strip()
            if len(full_q) >= 8:
                # Check if marks are embedded in full_q
                m_match = marks_regex.search(full_q)
                if m_match:
                    detected_m = normalize_marks(int(m_match.group(1)))
                else:
                    detected_m = marks
                questions.append({
                    "question_number": q_num or str(len(questions) + 1),
                    "question_text": full_q,
                    "suggested_marks": detected_m,
                    "unit_context": unit
                })

        current_q_num = None
        current_q_text = []
        current_marks = 5

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            # Check for Unit changes
            unit_match = unit_regex.search(line)
            if unit_match and len(line) < 70:
                # Flush previous question before starting new unit
                save_current_question(current_q_num, current_q_text, current_marks, current_unit)
                current_q_text = []
                current_unit = f"Unit {unit_match.group(1).upper()}"
                continue

            # Check for question start
            q_match = q_start_regex.match(line)
            if q_match:
                # Flush previous question
                save_current_question(current_q_num, current_q_text, current_marks, current_unit)
                
                # New question
                current_q_num = q_match.group(1) or q_match.group(2) or q_match.group(3) or str(len(questions) + 1)
                q_body = q_match.group(4).strip()
                
                # Check marks in this initial line
                m_match = marks_regex.search(line)
                if m_match:
                    current_marks = normalize_marks(int(m_match.group(1)))
                else:
                    current_marks = 5

                current_q_text = [q_body]
            else:
                # Continuation line
                if current_q_text and len(current_q_text) < 15:
                    if not line.startswith("Page ") and "Hall Ticket" not in line and "Roll No" not in line:
                        current_q_text.append(line)

        # Flush final question
        save_current_question(current_q_num, current_q_text, current_marks, current_unit)

        # Fallback if no numbered questions detected: split sentences ending with ?
        if not questions:
            sentences = re.split(r'(?<=[.?])\s+', text)
            q_idx = 1
            for s in sentences:
                s_clean = s.strip()
                if ('?' in s_clean or any(s_clean.lower().startswith(w) for w in ['explain', 'describe', 'what is', 'define', 'discuss', 'differentiate', 'compare', 'illustrate', 'write a short note'])) and len(s_clean) > 15:
                    questions.append({
                        "question_number": str(q_idx),
                        "question_text": s_clean,
                        "suggested_marks": 5,
                        "unit_context": "General"
                    })
                    q_idx += 1
                    if len(questions) >= 20:
                        break

        return questions
