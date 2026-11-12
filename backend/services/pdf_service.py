import os
import re
from io import BytesIO
from typing import Optional, Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Attempt to register Unicode / Telugu font
TELUGU_FONT_AVAILABLE = False
TELUGU_FONT_NAME = 'Helvetica'

def init_telugu_fonts():
    global TELUGU_FONT_AVAILABLE, TELUGU_FONT_NAME
    candidate_paths = [
        (r'C:\Windows\Fonts\Nirmala.ttc', 0),
        (r'C:\Windows\Fonts\Nirmala.ttf', None),
        (r'C:\Windows\Fonts\gautami.ttf', None),
        (r'C:\Windows\Fonts\mandali.ttf', None),
        (r'/usr/share/fonts/truetype/noto/NotoSansTelugu-Regular.ttf', None)
    ]

    for path, sub_idx in candidate_paths:
        if os.path.exists(path):
            try:
                if sub_idx is not None:
                    font = TTFont('TeluguUnicode', path, subfontIndex=sub_idx)
                else:
                    font = TTFont('TeluguUnicode', path)
                pdfmetrics.registerFont(font)
                TELUGU_FONT_AVAILABLE = True
                TELUGU_FONT_NAME = 'TeluguUnicode'
                break
            except Exception as e:
                continue

init_telugu_fonts()

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header banner
        self.drawString(54, 755, "AI STUDY MATE — Comprehensive Academic Study Notes")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 747, 558, 747)

        # Footer banner
        self.line(54, 45, 558, 45)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.drawString(54, 32, "Confidential — For Student Academic Preparation")
        self.restoreState()

class PDFService:
    @staticmethod
    def generate_note_pdf(
        title: str,
        content: str,
        subject: Optional[str] = None,
        unit: Optional[str] = None,
        marks: Optional[int] = None,
        language_mode: str = 'en'
    ) -> bytes:
        """
        Creates a beautifully formatted academic PDF document.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=68,
            bottomMargin=58
        )

        font_family = TELUGU_FONT_NAME if TELUGU_FONT_AVAILABLE else 'Helvetica'

        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=6,
            fontStyle='bold'
        )

        h2_style = ParagraphStyle(
            'H2Style',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#6C63FF'),
            spaceBefore=10,
            spaceAfter=4,
            fontStyle='bold'
        )

        h3_style = ParagraphStyle(
            'H3Style',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0F766E'),
            spaceBefore=8,
            spaceAfter=3,
            fontStyle='bold'
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName=font_family,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=6
        )

        bullet_style = ParagraphStyle(
            'Bullet',
            parent=body_style,
            leftIndent=15,
            bulletIndent=5,
            spaceAfter=3
        )

        code_style = ParagraphStyle(
            'CodeBlock',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor('#1E1B4B'),
            backColor=colors.HexColor('#F1F5F9'),
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=6
        )

        quote_style = ParagraphStyle(
            'Quote',
            parent=body_style,
            fontName=font_family,
            textColor=colors.HexColor('#0F766E'),
            backColor=colors.HexColor('#F0FDFA'),
            borderPadding=6,
            leftIndent=10,
            spaceBefore=4,
            spaceAfter=6
        )

        elements = []

        # Document Title
        clean_title = re.sub(r'[\r\n]+', ' ', title).strip()
        elements.append(Paragraph(clean_title, title_style))

        # Metadata Table
        meta_data = [
            [
                Paragraph(f"<b>Subject:</b> {subject or 'General Studies'}", body_style),
                Paragraph(f"<b>Unit:</b> {unit or 'General Module'}", body_style)
            ],
            [
                Paragraph(f"<b>Target Evaluation:</b> {marks or 5} Marks", body_style),
                Paragraph(f"<b>Language:</b> {'Telugu' if language_mode == 'te' else 'English + Telugu' if language_mode == 'en_te' else 'English'}", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[250, 250])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # Warning banner if Telugu text is present but font is missing
        has_telugu_text = any(ord(char) >= 0x0C00 and ord(char) <= 0x0C7F for char in content)
        if has_telugu_text and not TELUGU_FONT_AVAILABLE:
            warn_p = Paragraph(
                "<b>Warning:</b> Unicode Telugu font is not detected on this server. Telugu characters may display as approximations.",
                quote_style
            )
            elements.append(warn_p)
            elements.append(Spacer(1, 6))

        # Parse content paragraphs
        lines = content.split('\n')
        in_code_block = False
        code_lines = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            if trimmed.startswith('```'):
                if in_code_block:
                    # Flush code block
                    code_text = "<br/>".join([c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for c in code_lines])
                    elements.append(Paragraph(code_text, code_style))
                    code_lines = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue

            if in_code_block:
                code_lines.append(trimmed)
                continue

            # Markdown Headers
            if trimmed.startswith('### '):
                h_text = trimmed.replace('### ', '').strip()
                elements.append(Paragraph(h_text, h2_style))
            elif trimmed.startswith('## '):
                h_text = trimmed.replace('## ', '').strip()
                elements.append(Paragraph(h_text, h2_style))
            elif trimmed.startswith('# '):
                h_text = trimmed.replace('# ', '').strip()
                elements.append(Paragraph(h_text, h2_style))
            elif trimmed.startswith('- ') or trimmed.startswith('* '):
                b_text = trimmed[2:].strip()
                # Bold tags in bullets
                b_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', b_text)
                elements.append(Paragraph(f"&bull; {b_text}", bullet_style))
            elif trimmed.startswith('> '):
                q_text = trimmed[2:].strip()
                q_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', q_text)
                elements.append(Paragraph(q_text, quote_style))
            else:
                p_text = trimmed
                p_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', p_text)
                p_text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', p_text)
                elements.append(Paragraph(p_text, body_style))

        # Flush remaining code if any
        if code_lines:
            code_text = "<br/>".join([c.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') for c in code_lines])
            elements.append(Paragraph(code_text, code_style))

        # Build PDF with two-pass canvas
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer.getvalue()
