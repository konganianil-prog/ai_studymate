# 🚀 AI STUDY MATE — Complete AI-Powered Learning Platform

**AI STUDY MATE** is a full-stack, responsive, intelligent educational platform designed for university students, educators, and competitive exam aspirants. It transforms course documents, question papers, and study materials into structured examination answers (2, 5, 7, and 10 marks), provides bilingual English & Telugu explanations, interactive Three.js 3D learning models, Mermaid flowcharts and mind maps, AI-generated quizzes, spaced repetition flashcards, and formatted PDF study notes.

---

## 🌟 Key Features

1. **📄 Document Processing & Question Extraction**
   - Upload **PDF**, **DOCX**, and **TXT** question papers and lecture notes (up to 20MB).
   - High-performance text extraction using **PyMuPDF** (`pymupdf`) with **pypdf** fallback.
   - Built-in OCR hook for scanned PDF documents using Tesseract.
   - Intelligent question extraction engine that detects question numbers, unit modules, and suggested marks.
   - Select individual extracted questions with one click to generate complete answers.

2. **🤖 Multi-Tiered AI Answer Generation (2, 5, 7, and 10 Marks)**
   - **2 Marks:** Accurate academic definition, two critical points, and concise example.
   - **5 Marks:** Introduction, structured core explanation, bullet points, real-world example, and conclusion.
   - **7 Marks:** Detailed explanation, procedural working, exam diagram recommendation, advantages, and applications.
   - **10 Marks:** Architectural blueprint, step-by-step operational workflow, flowchart suggestions, advantages, disadvantages, industry use cases, and conclusion.
   - Edit, regenerate, and save generated answers directly into your personal Study Notes.

3. **🌐 Bilingual Explanations (English & Telugu)**
   - **English:** High-standard academic English.
   - **Telugu (తెలుగు):** Beginner-friendly, easy-to-understand Telugu explanations.
   - **English + Telugu:** Dual-mode showing complete technical answers in English followed by conversational Telugu concepts.

4. **🧊 Interactive 3D Educational Lab (Three.js)**
   - Real-time 3D models with 360&deg; rotation, mouse wheel zoom, pan, and fullscreen mode.
   - **Model Registry supporting 8 core topics:**
     - ⚛️ **Atom Structure:** Bohr atomic model with nucleus and animated orbiting electron shells.
     - 🧬 **DNA Helix:** Double-stranded antiparallel polymer with base pair rungs (A-T, G-C).
     - 🫀 **Human Heart:** Chambered cardiac model with ventricles, aorta, and pulsating rhythm.
     - 🧠 **Human Brain:** Left and right cerebral hemispheres, cerebellum, and brainstem.
     - 🪐 **Solar System:** Sun with coronal glow and animated planetary orbits.
     - 💻 **CPU Architecture:** Silicon multi-core processor, heat spreader, and gold contact pins.
     - 🌐 **Network Topology:** Star network switch with workstations, server rack, and transmission lines.
     - 🔗 **Blockchain Structure:** Cryptographically linked blocks with floating data payload cubes.
   - Wireframe mode toggle and step-by-step anatomical & architectural breakdown cards.

5. **📊 Visual Explainer, Flowcharts & Mind Maps**
   - Visual diagrams powered by **Mermaid.js**.
   - Topic-based flowcharts, process workflows, and hierarchical mind maps.
   - Export diagrams directly as **PNG** or **SVG** image files.
   - Custom educational SVG schematics for core computing and science concepts.

6. **🎯 AI Quiz Generator & Practice Mode**
   - Generate 4-choice Multiple Choice Questions (MCQs) from study topics or uploaded documents.
   - Difficulty tiers: **Easy**, **Medium**, **Hard**.
   - **Exam Mode:** Answer all questions, submit, and receive detailed score analytics and rationales.
   - **Practice Mode:** Instant feedback on each question.
   - Track score history and view past quiz attempts.

7. **🗂️ Spaced Repetition Flashcards**
   - 3D flip card animation with keyword/term on the front and concise definition on the back.
   - Mark cards as **Mastered** (Known) or **Need Revision**.
   - Deck progress indicators and saved flashcard collections.

8. **📝 Study Notes & PDF Export with Unicode Telugu Support**
   - Create, edit, tag, search, and pin study notes organized by Subject and Unit.
   - Export formatted academic study notes as PDF using **ReportLab**.
   - Dynamic two-pass page numbering ("Page X of Y"), clean tables, and code formatting.
   - **Telugu Unicode Support:** Uses Windows native `Nirmala.ttc` font for rendering Telugu text without character corruption.

9. **🔒 Secure User Authentication & Dashboard Analytics**
   - User registration and login with secure password hashing (`werkzeug.security`).
   - Session management with protected routes (`Flask-Login`).
   - Dashboard statistics: Total documents, generated answers, saved notes, and average quiz scores.
   - Interactive Chart.js performance trends.
   - Dark and Light theme toggle with local storage persistence.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons, Three.js, OrbitControls, Chart.js, Mermaid.js |
| **Backend** | Python 3.12, Flask, Flask-Login, Flask-CORS, Flask-SQLAlchemy |
| **Database** | SQLite, SQLAlchemy ORM |
| **AI Integration** | Google Gen AI SDK (`google-genai`) with offline educational generator fallback |
| **Document Processing** | PyMuPDF (`pymupdf`), `python-docx`, `pypdf`, OCR hook via `pytesseract` |
| **PDF Generation** | ReportLab with Unicode Font Registration (`Nirmala.ttc`) |
| **Testing** | PyTest (23 automated unit and integration tests) |

---

## 📂 Project Structure

```
ai_studymate/
│
├── backend/
│   ├── app.py                      # Application factory & setup
│   ├── config.py                   # Configuration & environment loader
│   ├── extensions.py               # SQLAlchemy & LoginManager instances
│   │
│   ├── models/
│   │   ├── __init__.py             # Model exports & default subject seed data
│   │   ├── user.py                 # User authentication model
│   │   ├── document.py             # Document & ExtractedQuestion models
│   │   ├── subject.py              # Subject & Unit models
│   │   ├── answer.py               # GeneratedAnswer & GeneratedVisual models
│   │   ├── quiz.py                 # Quiz, QuizQuestion, QuizAttempt, Flashcard
│   │   └── note.py                 # StudyNote model
│   │
│   ├── routes/
│   │   ├── __init__.py             # Route blueprint registrations
│   │   ├── auth.py                 # User authentication (register, login, logout)
│   │   ├── main.py                 # Views, dashboard, global search, stats API
│   │   ├── documents.py            # Upload, document text extraction & questions
│   │   ├── answers.py              # 2, 5, 7, 10-marks AI answer generation
│   │   ├── visuals.py              # Flowcharts, mind maps & educational visuals
│   │   ├── quizzes.py              # Quizzes & Flashcards APIs
│   │   ├── notes.py                # Study notes CRUD & PDF export
│   │   └── subjects.py             # Subjects & Units management
│   │
│   ├── services/
│   │   ├── ai_service.py           # Google Gemini AI & offline template engine
│   │   ├── document_service.py     # PDF, DOCX, TXT parser & question extractor
│   │   ├── image_service.py        # Educational SVG diagram generator
│   │   ├── quiz_service.py         # MCQ and Flashcard generator
│   │   └── pdf_service.py          # ReportLab PDF generator with Telugu fonts
│   │
│   └── utils/
│       └── helpers.py              # Safe filenames, file validator, JSON responder
│
├── frontend/
│   ├── templates/
│   │   ├── base.html               # Master layout (sidebar, topbar, theme toggle)
│   │   ├── index.html              # Landing page
│   │   ├── login.html              # Sign in page
│   │   ├── register.html           # Registration page
│   │   ├── dashboard.html          # Dashboard with analytics & quick actions
│   │   ├── upload.html             # Document upload & question extractor
│   │   ├── answers.html            # AI Answer Lab (2, 5, 7, 10 marks & Telugu)
│   │   ├── visualizer.html         # Flowcharts & mind map generator
│   │   ├── 3d-lab.html             # Interactive 3D Three.js learning lab
│   │   ├── quiz.html               # Practice & exam quizzes
│   │   ├── flashcards.html         # 3D Flip flashcards
│   │   ├── notes.html              # Study notes management & PDF export
│   │   └── subjects.html           # Subject & Unit syllabus manager
│   │
│   └── static/
│       ├── css/
│       │   └── style.css           # Premium glassmorphic styles (dark/light)
│       └── js/
│           ├── main.js             # Global theme, search, notifications
│           └── three_lab.js        # Three.js 3D models & OrbitControls
│
├── uploads/                        # Secure storage for uploaded documents
├── generated/                      # Generated educational illustrations & SVGs
├── tests/
│   ├── test_phase1.py              # App startup, database, models, auth
│   ├── test_phase2.py              # File upload, text extraction, question parser
│   ├── test_phase3.py              # 2, 5, 7, 10-marks answers & Telugu modes
│   ├── test_phase4.py              # Visual concepts, flowcharts & SVG generation
│   ├── test_phase5.py              # 3D Lab route protection & 8-model registry
│   └── test_phase6.py              # Quizzes, scoring, flashcards, ReportLab PDF
│
├── run.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .env                            # Local environment configuration
├── DEVELOPMENT_PROGRESS.md         # Phased implementation log
└── README.md                       # Documentation & instructions
```

---

## ⚡ Prerequisites

- **Windows 10 / Windows 11**
- **Python 3.10+** (Python 3.12 recommended)
- **PowerShell** or **Command Prompt**

---

## 🚀 Installation & Setup (Windows)

### 1. Open Terminal in Project Directory
Open **PowerShell** and navigate to the project directory:
```powershell
cd c:\Users\konga\OneDrive\Desktop\ai_studymate
```

### 2. Verify Python Installation
```powershell
python --version
```

### 3. Install Required Dependencies
Run:
```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` (already created for local development):
```powershell
Copy-Item .env.example .env
```

Open `.env` in any text editor and optionally add your **Google Gemini API Key**:
```env
SECRET_KEY=dev-secret-key-ai-studymate-2026-secure
DATABASE_URL=sqlite:///study_mate.db
GEMINI_API_KEY=your_gemini_api_key_here
MAX_CONTENT_LENGTH=20971520
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```
> [!NOTE]
> **No API Key? No Problem!**
> The application will still start and operate completely without an API key. In offline mode, the intelligent educational template engine generates high-quality, structured academic answers, flowcharts, quizzes, and flashcards so you can test and use all features immediately!

---

## 🖥️ Running the Application

To launch AI STUDY MATE, run:
```powershell
python run.py
```

You will see:
```text
============================================================
  🚀 AI STUDY MATE - Intelligent Learning Platform
  🌐 Running at: http://127.0.0.1:5000
============================================================
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Running Automated Tests

To run the complete test suite (23 tests across all 6 phases):
```powershell
python -m pytest tests/ -v
```

All tests mock external AI calls and run locally using an in-memory SQLite database, requiring zero API credits.

---

## 📖 How to Use AI STUDY MATE

### Step 1: Create an Account
1. Open [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register).
2. Enter your Full Name, Username, Email, and Password.
3. You will be automatically signed in and redirected to the **Dashboard**.

### Step 2: Upload Question Papers & Documents
1. Navigate to **Upload Materials** (`/upload`) in the sidebar.
2. Drag and drop any `.pdf`, `.docx`, or `.txt` question paper or study sheet.
3. Click **Upload & Extract Questions**.
4. The system parses the document, displays the full text, and extracts all detected examination questions with their suggested marks (2, 5, 7, 10).
5. Click **Generate Answer** next to any question to load it directly into the AI Answer Lab.

### Step 3: Generate 2, 5, 7, and 10 Marks Answers
1. Go to **AI Answer Lab** (`/answers`).
2. Enter a question manually or pick one extracted from your uploaded documents.
3. Select your desired marks: **2 Marks**, **5 Marks**, **7 Marks**, or **10 Marks**.
4. Choose the language: **English**, **Telugu**, or **English + Telugu**.
5. Click **Generate Structured Answer**.
6. The answer is presented with headings, bullet points, and diagram suggestions.
7. Click **Edit** to make personal modifications, or **Save Note** to add it directly to your study notes!

### Step 4: Explore the 3D Learning Lab
1. Go to **3D Learning Lab** (`/3d-lab`).
2. Select any of the 8 educational topics from the bottom strip:
   - *Atom & Bohr Model*, *DNA Helix*, *Human Heart*, *Human Brain*, *Solar System*, *CPU Processor*, *Network Topology*, *Blockchain Ledger*.
3. Click and drag with the left mouse button to rotate 360&deg;.
4. Scroll to zoom in and out.
5. Use the toolbar to toggle wireframe mode, auto-rotation, or view in fullscreen.
6. Read the detailed component breakdown and anatomical annotations on the right.

### Step 5: Visual Learning & Flowcharts
1. Go to **Visual & Flowcharts** (`/visualizer`).
2. Enter any concept (e.g., *Blockchain*, *Convolutional Neural Networks*, *Deadlock*).
3. Select **Flowchart** or **Mind Map**.
4. Click **Generate Visual Explainer**.
5. View the interactive diagram, inspect step-by-step workflow stages, and click **Download PNG** or **Download SVG**.

### Step 6: Practice AI Quizzes
1. Go to **AI Quiz Practice** (`/quiz`).
2. Enter a topic or choose an uploaded question paper.
3. Select difficulty (**Easy**, **Medium**, **Hard**) and question count (5 or 10).
4. Answer the multiple choice questions and click **Submit & Check Score**.
5. Review your score percentage, answer breakdown, and explanation for every question.

### Step 7: Flashcards & Revision
1. Go to **Flashcards** (`/flashcards`).
2. Click **Generate Flashcard Deck** and enter a topic.
3. Click on the 3D card to flip between Question and Answer.
4. Mark cards as **Mastered** or **Need Revision** to track retention.

### Step 8: Study Notes & PDF Export
1. Go to **Study Notes & PDF** (`/notes`).
2. Search and organize your notes by Subject and Unit.
3. Click the **PDF** button on any note to download a clean, publication-ready academic revision sheet with Unicode Telugu support.

---

## 🛡️ Security Features
- **Password Protection:** Werkzeug PBKDF2/SHA-256 password hashing.
- **File Validation:** Strict MIME and file extension validation preventing execution of unauthorized scripts.
- **Path Traversal Protection:** Unique UUID prefixes and sanitized filenames (`secure_filename`).
- **Secret Management:** Environment variable separation (`.env`) ensuring zero API keys or secret credentials in client-side code.
- **SQL Injection Prevention:** 100% parameterized queries via SQLAlchemy ORM.

---

## 📜 License
This project is developed for educational learning and examination preparation purposes.
