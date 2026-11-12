import os
import re
import json
from typing import Dict, Any, Optional

class AIService:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY', '').strip()
        self.model_name = model_name or os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[AIService] Failed to initialize Google GenAI client: {e}")
                self.client = None

    def is_configured(self) -> bool:
        return bool(self.client and self.api_key)

    def generate_visual_concept(self, topic: str) -> Dict[str, Any]:
        """
        Generates structured visual learning artifacts for a topic:
        - Concept explanation
        - Important points
        - Step-by-step workflow
        - Real-world example
        - Mermaid flowchart definition
        - Mermaid mindmap definition
        """
        topic_clean = topic.strip()
        topic_lower = topic_clean.lower()

        # If Gemini is live, try generating customized Mermaid diagram
        if self.is_configured():
            try:
                prompt = f"""
You are an expert computer science and engineering visual educator.
Create a visual learning breakdown for the topic: "{topic_clean}".

Respond in JSON with this exact schema:
{{
  "explanation": "Clear 2-3 paragraph academic explanation of {topic_clean}",
  "key_points": ["point 1", "point 2", "point 3", "point 4"],
  "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ...", "Step 4: ..."],
  "real_world_example": "A concrete real-world implementation example",
  "mermaid_flowchart": "graph TD\\n  A[Start] --> B[Step 1]\\n  ...",
  "mermaid_mindmap": "mindmap\\n  root(({topic_clean}))\\n    Core Principles\\n      Principle 1\\n    Components\\n      Comp 1\\n    Applications\\n      App 1"
}}
Return only valid JSON.
"""
                resp = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                text = resp.text.strip()
                if text.startswith("```"):
                    text = re.sub(r"^```(?:json)?\s*", "", text)
                    text = re.sub(r"\s*```$", "", text)
                data = json.loads(text)
                data['is_ai_live'] = True
                return data
            except Exception as e:
                print(f"[AIService] Visual generation via Gemini failed, using fallback: {e}")

        # Deterministic rich fallback generator for standard curriculum topics
        flowchart = f"""graph TD
    A[Start: {topic_clean} Ingestion] --> B[Data Validation & Preprocessing]
    B --> C[Core Algorithmic Execution]
    C --> D{{Verification Check}}
    D -- Success --> E[State Persistence & Output Synthesis]
    D -- Retry / Fallback --> B
    E --> F[End / Client Response]
"""

        mindmap = f"""mindmap
  root(({topic_clean}))
    Theoretical Foundations
      Mathematical Invariants
      Complexity Bounds
      Formal Model
    Core Architecture
      Input Buffer
      Processing Engine
      State Storage
    Key Advantages
      High Throughput
      Fault Isolation
      Modular Scalability
    Industry Applications
      Distributed Cloud
      Enterprise Systems
      Autonomous AI
"""

        steps = [
            f"Initialization: Setup internal states and parameters required for {topic_clean}.",
            "Transformation: Process incoming payloads using the core algorithmic logic.",
            "Verification: Ensure constraints and safety checks are satisfied.",
            "Commitment: Finalize output, update state caches, and return telemetry."
        ]

        key_points = [
            f"Fundamental paradigm in modern computational engineering.",
            f"Ensures deterministic performance with minimal overhead.",
            f"Provides modular isolation across subsystems.",
            f"Widely adopted in large-scale mission-critical infrastructure."
        ]

        explanation = f"**{topic_clean}** is an essential computational paradigm designed to coordinate resource allocation, process flow, and system state transitions. By modularizing complex operational logic, it ensures high reliability, maintainability, and predictable latency across distributed environments."

        real_world = f"In contemporary production architectures, **{topic_clean}** is applied within high-throughput message brokers (such as Apache Kafka), kernel task dispatchers, and distributed databases to prevent race conditions and guarantee high availability."

        return {
            "explanation": explanation,
            "key_points": key_points,
            "steps": steps,
            "real_world_example": real_world,
            "mermaid_flowchart": flowchart,
            "mermaid_mindmap": mindmap,
            "is_ai_live": False
        }

    def generate_answer(
        self,
        question_text: str,
        marks: int = 5,
        language_mode: str = "en",
        subject_name: Optional[str] = None,
        unit_title: Optional[str] = None,
        context_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a structured exam answer matching 2, 5, 7, or 10 marks criteria.
        language_mode: 'en' (English), 'te' (Telugu), 'en_te' (English + Telugu)
        """
        if self.is_configured():
            try:
                return self._generate_with_gemini(
                    question_text, marks, language_mode, subject_name, unit_title, context_text
                )
            except Exception as e:
                print(f"[AIService] Gemini API error, falling back to offline generator: {e}")
                return self._generate_fallback(
                    question_text, marks, language_mode, subject_name, unit_title, context_text,
                    note=f"Notice: Generated using offline educational engine (API response: {str(e)})"
                )
        else:
            return self._generate_fallback(
                question_text, marks, language_mode, subject_name, unit_title, context_text,
                note="Notice: Generated using offline educational template engine. Set GEMINI_API_KEY in .env for live Gemini AI."
            )

    def _generate_with_gemini(
        self,
        question_text: str,
        marks: int,
        language_mode: str,
        subject: Optional[str],
        unit: Optional[str],
        context: Optional[str]
    ) -> Dict[str, Any]:
        """Calls Google GenAI API to produce structured academic output."""
        structure_guide = {
            2: "Definition, Two important points, Short example if required.",
            5: "Introduction, Core Explanation, Important points (bullet points), Practical example, Short conclusion.",
            7: "Introduction, Detailed explanation, Working or process, Diagram suggestion, Key advantages and applications, Conclusion.",
            10: "Introduction, Detailed architectural/conceptual explanation, Architecture or working process, Step-by-step workflow, Diagram or flowchart suggestion, Advantages, Disadvantages, Real-world applications, Conclusion."
        }.get(marks, "Introduction, Explanation, Key Points, Conclusion.")

        lang_instruction = {
            'en': "Generate the entire answer in high-standard academic English.",
            'te': "Explain the concept thoroughly in simple, beginner-friendly Telugu (తెలుగు). Keep technical terms, formulas and code readable in English with Telugu explanation.",
            'en_te': "First generate the complete technical academic answer in English. Then provide a dedicated 'Telugu Explanation' section that explains the concept in simple conversational Telugu for quick understanding."
        }.get(language_mode, "Generate in academic English.")

        prompt = f"""
You are AI STUDY MATE, a university professor and exam evaluator.
A student needs an answer for the following exam question:

Question: {question_text}
Target Marks: {marks} Marks
Subject: {subject or 'General Engineering / Science'}
Unit / Module: {unit or 'General'}
Relevant Study Material Context: {context[:1500] if context else 'None provided'}

Strict Answer Requirements:
- Strictly follow the required structure for {marks} marks:
  {structure_guide}
- Language requirement: {lang_instruction}
- Use markdown headings (###, ####), bullet points, and clear technical explanations.
- Do NOT hallucinate facts or fake references.
- Suggest a concrete diagram or flowchart where applicable.
- If language_mode is 'en_te', clearly separate the English answer from the Telugu explanation.

Respond in JSON with the following format:
{{
  "english_answer": "Complete English answer in formatted markdown",
  "telugu_explanation": "Telugu explanation if language_mode is 'te' or 'en_te', else empty string",
  "diagram_suggestion": "Description of recommended diagram or ASCII/flowchart outline",
  "key_points": ["bullet 1", "bullet 2", "bullet 3"]
}}
Return only valid JSON.
"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        resp_text = response.text.strip()
        # Clean JSON markdown if wrapped in ```json
        if resp_text.startswith("```"):
            resp_text = re.sub(r"^```(?:json)?\s*", "", resp_text)
            resp_text = re.sub(r"\s*```$", "", resp_text)

        try:
            data = json.loads(resp_text)
            raw = data.get("english_answer", "")
            if language_mode == 'te' and data.get("telugu_explanation"):
                raw = data.get("telugu_explanation")
            elif language_mode == 'en_te' and data.get("telugu_explanation"):
                raw = f"{raw}\n\n### 🇮🇳 తెలుగు వివరణ (Telugu Explanation)\n{data.get('telugu_explanation')}"

            return {
                "raw_answer": raw,
                "telugu_explanation": data.get("telugu_explanation", ""),
                "diagram_suggestion": data.get("diagram_suggestion", ""),
                "key_points": data.get("key_points", []),
                "is_ai_live": True
            }
        except Exception:
            # If JSON parsing fails, use the raw response text
            return {
                "raw_answer": resp_text,
                "telugu_explanation": "",
                "diagram_suggestion": "Refer to the diagram outline described in the text.",
                "key_points": [f"Key point for {marks} marks"],
                "is_ai_live": True
            }

    def _generate_fallback(
        self,
        question_text: str,
        marks: int,
        language_mode: str,
        subject: Optional[str],
        unit: Optional[str],
        context: Optional[str],
        note: str = ""
    ) -> Dict[str, Any]:
        """
        High quality, structured offline educational fallback engine.
        Guarantees that 2, 5, 7, and 10 marks formats are fully respected.
        """
        topic = question_text.strip().rstrip('?.:')
        subj = subject or "Computer Science & Engineering"

        # Generate mark-specific content
        if marks == 2:
            raw_en = f"""### Definition
**{topic}** is a fundamental concept in {subj} that defines the structural or operational mechanism used to solve computational and analytical problems efficiently.

### Key Points
- **Primary Objective:** Establishes predictable execution behavior and ensures system integrity and modularity.
- **Critical Characteristic:** Minimizes algorithmic overhead while maintaining determinism, security, and scalability.

### Example
For instance, in a real-world system, `{topic}` is utilized to coordinate state transitions and synchronize resource distribution across active nodes.
"""
            telugu = f"**{topic}** అనేది {subj} లో ఒక ముఖ్యమైన భావన. ఇది కంప్యూటేషనల్ సమస్యలను సమర్థవంతంగా పరిష్కరించడానికి మరియు సిస్టమ్ వేగాన్ని పెంచడానికి ఉపయోగపడుతుంది. ఉదాహరణకు, సిస్టమ్ లోని వివిధ భాగాల మధ్య సమన్వయం సాధించడానికి దీనిని వాడతారు."

        elif marks == 5:
            raw_en = f"""### 1. Introduction
**{topic}** plays a pivotal role in {subj}. It provides an organized framework that balances operational efficiency, correctness, and resource utilization.

### 2. Core Explanation
At its core, **{topic}** operates by decomposing complex interactions into well-defined, verifiable stages:
1. **Input Representation:** Structured data or state vectors are gathered and validated against system constraints.
2. **Processing & Transformation:** The core logic evaluates dependencies, resolves conflicts, and produces intermediate transformations.
3. **Execution & Feedback:** The final state is committed, providing deterministic output and actionable telemetry.

### 3. Important Points
- **Efficiency:** Drastically reduces redundant computational cycles.
- **Robustness:** Handles boundary cases and unexpected exceptions gracefully.
- **Maintainability:** Facilitates modular architecture and easy unit testing.

### 4. Practical Example
In modern software systems, **{topic}** is deployed in microservices pipelines, transaction coordinators, and operating system kernels to manage concurrent tasks without deadlocks.

### 5. Conclusion
Mastery of {topic} is essential for designing resilient, high-throughput architectures in contemporary computing environments.
"""
            telugu = f"""**పరిచయం & వివరణ ({topic}):**
{topic} అనేది {subj} లో అత్యంత కీలకమైన అంశం. ఇది సంక్లిష్టమైన సమస్యలను సరళమైన దశలుగా విభజించి సులభంగా పరిష్కరిస్తుంది.

**ముఖ్యమైన లక్షణాలు:**
- పనితీరును మరియు వేగాన్ని పెంచుతుంది.
- లోపాలు (errors) రాకుండా సిస్టమ్ ను స్థిరంగా ఉంచుతుంది.
- సులభంగా అర్థం చేసుకునేందుకు మరియు అభివృద్ధి చేసేందుకు అనుకూలంగా ఉంటుంది.

**ముగింపు:** ఈ కాన్సెప్ట్ అర్థం చేసుకోవడం ద్వారా ఆధునిక సాఫ్ట్‌వేర్ మరియు హార్డ్‌వేర్ ఆర్కిటెక్చర్‌లను సమర్థవంతంగా రూపొందించవచ్చు."""

        elif marks == 7:
            raw_en = f"""### 1. Introduction
In {subj}, **{topic}** is recognized as a cornerstone methodology designed to address scalability, throughput, and system reliability. It directly impacts how computational resources are allocated and optimized.

### 2. Detailed Explanation & Theoretical Principles
The operational paradigm of **{topic}** is governed by standard academic principles:
- **State Invariance:** Ensures that internal invariants remain intact before and after every lifecycle event.
- **Resource Management:** Dynamically allocates memory, CPU cycles, and network bandwidth according to priority tiers.
- **Decoupled Architecture:** Separates control logic from presentation and storage layers.

### 3. Working & Process Workflow
The procedural workflow comprises four sequential phases:
```
[Phase 1: Initialization & Parameter Validation]
                     │
                     ▼
[Phase 2: Core Algorithmic Execution & Evaluation]
                     │
                     ▼
[Phase 3: Verification & Invariant Checking]
                     │
                     ▼
[Phase 4: Output Synthesis & State Commitment]
```

### 4. Diagram Suggestion
*Recommended Exam Diagram:* Draw a modular block diagram with:
1. **Client / Sensor Ingestion Node** on the left.
2. **Processing & Coordination Engine ({topic})** in the center with internal state queues.
3. **Target Store / Database & Telemetry Bus** on the right with bidirectional arrows indicating acknowledgment signals.

### 5. Advantages & Practical Applications
- **Advantages:** High throughput, fault isolation, deterministic latency, and predictable scaling.
- **Applications:** Distributed databases, operating system kernel schedulers, deep neural network training pipelines, and secure financial transaction processing.

### 6. Conclusion
To summarize, **{topic}** provides the theoretical and practical foundation necessary for building robust, enterprise-grade engineering systems.
"""
            telugu = f"""**వివరమైన వివరణ ({topic}):**
{topic} అనేది సిస్టమ్ యొక్క వేగం, విశ్వసనీయత మరియు భద్రతను మెరుగుపరిచే ఒక ముఖ్యమైన విధానం.

**పనిచేసే విధానం:**
1. సమాచారాన్ని (Input) స్వీకరించి సరైనదో కాదో తనిఖీ చేస్తుంది.
2. అవసరమైన ప్రాసెసింగ్ చేసి ఫలితాన్ని సిద్ధం చేస్తుంది.
3. లోపాలు లేకుండా ధృవీకరించి ఫలితాన్ని (Output) అందిస్తుంది.

**ఉపయోగాలు మరియు ప్రయోజనాలు:**
- డేటా ప్రాసెసింగ్ వేగం చాలా ఎక్కువగా ఉంటుంది.
- నెట్‌వర్క్ మరియు సిస్టమ్ వనరులు వృధా కావు.
- పెద్ద ప్రాజెక్టులు మరియు పరిశ్రమలలో విస్తృతంగా వినియోగిస్తారు."""

        else:  # 10 Marks
            raw_en = f"""### 1. Introduction
**{topic}** represents one of the most comprehensive topics in {subj}. A deep understanding of its architectural foundations, algorithmic complexities, and design trade-offs is essential for university examinations and real-world system engineering.

### 2. Architectural Blueprint & Core Components
The complete architectural layout of **{topic}** consists of four cooperating subsystems:
- **Control Unit / Coordinator:** Interprets instructions, schedules execution queues, and enforces consistency policies.
- **Execution Engine:** Implements the underlying algorithmic transformations with optimized time complexity $\\mathcal{{O}}(n)$.
- **Memory & State Buffer:** Maintains volatile working states with synchronization primitives to prevent race conditions.
- **Interface & Communication Bus:** Facilitates standardized API exchanges and message serialization.

### 3. Step-by-Step Operational Workflow
```
+-----------------------------------------------------------+
| Step 1: Input Ingestion & Authentication                   |
| -> Validate headers, decode payloads, verify signatures   |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+
| Step 2: Scheduling & Resource Allocation                  |
| -> Assign execution priority and allocate memory chunks   |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+
| Step 3: Algorithmic Transformation ({topic})               |
| -> Execute core mathematical and logic pipelines          |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+
| Step 4: Verification, Logging & State Persistence         |
| -> Write-ahead logs, commit state, return ACK to client   |
+-----------------------------------------------------------+
```

### 4. Diagram & Flowchart Layout
*Exam Diagram Guidance:*
- Draw a clear rectangular box representing the main **{topic} Controller**.
- Inside, show sub-components: *Scheduler*, *Memory Management Unit*, *ALU / Logic Processor*, and *Output Filter*.
- Draw input arrows labeled `Incoming Stream / Query` and output arrows labeled `Processed Response`.
- Include a side bidirectional link to `Storage / Registry`.

### 5. Key Advantages
1. **High Scalability:** Scales horizontally across distributed clusters without single points of failure.
2. **Deterministic Response Times:** Predictable latency guarantees under heavy workload pressure.
3. **Fault Tolerance:** Automated checkpointing and recovery protocols restore state during node failures.
4. **Extensibility:** Plug-and-play architecture allows modular additions without breaking existing interfaces.

### 6. Limitations & Disadvantages
1. **Architectural Complexity:** Requires rigorous synchronization mechanisms and expert operational maintenance.
2. **Initial Overhead:** Setup latency and memory footprint can be non-trivial for small datasets.
3. **Debugging Overhead:** Tracing concurrent anomalies requires specialized distributed logging infrastructure.

### 7. Real-World Applications & Industry Use Cases
- **Cloud Infrastructure:** Kubernetes orchestration, AWS EC2 compute scheduling, and distributed load balancing.
- **Enterprise Databases:** Two-phase commit protocols, B-Tree index management, and transaction isolation.
- **AI & Data Engineering:** Tensor graph optimization, parameter servers in PyTorch/TensorFlow, and ETL pipelines.

### 8. Conclusion
In conclusion, **{topic}** represents an indispensable paradigm in modern computing. Its balanced synthesis of performance, reliability, and modularity makes it a foundational topic for both academic mastery and industrial system design.
"""
            telugu = f"""### 🇮🇳 10 మార్కుల సమగ్ర తెలుగు వివరణ ({topic})

**1. పరిచయం:**
{topic} అనేది కంప్యూటర్ సైన్స్ మరియు ఇంజనీరింగ్ లో ఒక ప్రాథమికమైన మరియు అత్యంత కీలకమైన అంశం. ఇది భారీ డేటా మరియు క్లిష్టమైన కంప్యూటింగ్ ప్రక్రియలను సులభతరం చేస్తుంది.

**2. సిస్టమ్ నిర్మాణం (Architecture):**
- **కంట్రోలర్ (Controller):** అన్ని భాగాలను పర్యవేక్షిస్తుంది.
- **ప్రాసెసింగ్ ఇంజిన్:** అల్గారిథమ్‌లను వేగంగా అమలు చేస్తుంది.
- **మెమరీ బఫర్:** తాత్కాలిక డేటాను భద్రపరుస్తుంది.
- **ఇంటర్‌ఫేస్:** యూజర్ లేదా ఇతర సిస్టమ్‌లతో కమ్యూనికేట్ చేయడానికి తోడ్పడుతుంది.

**3. ప్రయోజనాలు (Advantages):**
- అత్యధిక వేగం మరియు విశ్వసనీయత.
- భారీ మొత్తంలో డేటాను కూడా ఒకేసారి ప్రాసెస్ చేయగల సామర్థ్యం.
- భద్రత మరియు స్థిరత్వం చాలా ఎక్కువ.

**4. పరిమితులు (Disadvantages):**
- సిస్టమ్ డిజైన్ సంక్లిష్టంగా ఉంటుంది.
- ప్రారంభంలో సెటప్ చేయడానికి అధిక వనరులు అవసరం.

**5. వాస్తవ ప్రపంచంలో ఉపయోగాలు (Real-world Applications):**
- క్లౌడ్ కంప్యూటింగ్ (AWS, Google Cloud).
- బ్యాంకింగ్ మరియు ఫైనాన్షియల్ లావాదేవీల రక్షణ.
- ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ మరియు బిగ్ డేటా సిస్టమ్స్.

**ముగింపు:** ఈ కాన్సెప్ట్‌ను లోతుగా అర్థం చేసుకోవడం ద్వారా పరీక్షలలో మంచి మార్కులు సాధించడమే కాకుండా, నిజ జీవిత ప్రాజెక్ట్‌లను కూడా విజయవంతంగా నిర్మించవచ్చు."""

        if language_mode == 'te':
            final_raw = f"{telugu}\n\n> *{note}*" if note else telugu
        elif language_mode == 'en_te':
            final_raw = f"{raw_en}\n\n{telugu}\n\n> *{note}*" if note else f"{raw_en}\n\n{telugu}"
        else:
            final_raw = f"{raw_en}\n\n> *{note}*" if note else raw_en

        diagram_suggestion = f"Flowchart/Block Diagram depicting {topic} components, data input queues, processor engine, and output storage buffer."

        key_points = [
            f"Core definition and theoretical foundation of {topic}",
            f"Step-by-step workflow suited for {marks} marks evaluation",
            f"Architecture, advantages, and practical applications in {subj}"
        ]

        return {
            "raw_answer": final_raw,
            "telugu_explanation": telugu if language_mode in ('te', 'en_te') else "",
            "diagram_suggestion": diagram_suggestion,
            "key_points": key_points,
            "is_ai_live": False
        }
