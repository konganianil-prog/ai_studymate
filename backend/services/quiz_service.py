import json
import re
from typing import List, Dict, Any, Optional
from backend.services.ai_service import AIService

class QuizService:
    def __init__(self, ai_service: Optional[AIService] = None):
        self.ai = ai_service or AIService()

    def generate_quiz(
        self,
        topic: str,
        count: int = 5,
        difficulty: str = "medium",
        context_text: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates 4-option MCQs with exactly one correct answer and explanation.
        """
        if self.ai.is_configured():
            try:
                return self._generate_quiz_gemini(topic, count, difficulty, context_text)
            except Exception as e:
                print(f"[QuizService] Gemini quiz generation failed, using fallback: {e}")

        return self._generate_quiz_fallback(topic, count, difficulty)

    def _generate_quiz_gemini(
        self,
        topic: str,
        count: int,
        difficulty: str,
        context: Optional[str]
    ) -> List[Dict[str, Any]]:
        prompt = f"""
You are an examination question creator for university students.
Generate {count} multiple choice questions (MCQs) for the topic: "{topic}".
Difficulty: {difficulty} (easy / medium / hard).
Reference context: {context[:1500] if context else 'None provided'}.

Rules:
1. Each question must have exactly 4 choices: option_a, option_b, option_c, option_d.
2. Only ONE correct answer (correct_option: "A", "B", "C", or "D").
3. Include an academic explanation for why that option is correct.

Respond in JSON array format:
[
  {{
    "question_text": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_option": "A",
    "explanation": "..."
  }}
]
Return ONLY the JSON array.
"""
        resp = self.ai.client.models.generate_content(
            model=self.ai.model_name,
            contents=prompt
        )
        text = resp.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        data = json.loads(text)
        return data[:count]

    def _generate_quiz_fallback(self, topic: str, count: int, difficulty: str) -> List[Dict[str, Any]]:
        """Domain-aware fallback MCQs."""
        t_clean = topic.strip()
        diff_tag = difficulty.capitalize()

        templates = [
            {
                "question_text": f"Which of the following best defines the primary objective of {t_clean}?",
                "option_a": f"To optimize resource utilization and maintain deterministic state transitions.",
                "option_b": f"To permanently bypass hardware memory validation checks.",
                "option_c": f"To eliminate the need for operating system CPU scheduling.",
                "option_d": f"To convert all relational schemas into unindexed linear lists.",
                "correct_option": "A",
                "explanation": f"{t_clean} is specifically engineered to ensure system stability, predictability, and optimized throughput."
            },
            {
                "question_text": f"In the context of {t_clean}, what is the main consequence of improper synchronization?",
                "option_a": f"Deterministic execution speed increases by 50%.",
                "option_b": f"Race conditions, data inconsistency, and deadlock vulnerability.",
                "option_c": f"Automatic conversion to single-cycle microcode.",
                "option_d": f"Memory buffers become completely immutable.",
                "correct_option": "B",
                "explanation": "In concurrent operations, improper synchronization inevitably triggers race conditions or deadlock anomalies."
            },
            {
                "question_text": f"What is the theoretical worst-case time complexity typically associated with standard operations in {t_clean}?",
                "option_a": "O(1) constant time across all workloads",
                "option_b": "O(n) or O(n log n) depending on underlying data structures",
                "option_c": "O(2^n) exponential for basic lookups",
                "option_d": "O(0) zero compute overhead",
                "correct_option": "B",
                "explanation": "Standard balanced search and traversal architectures operate within logarithmic or linear bounds."
            },
            {
                "question_text": f"Which architectural layer is primarily responsible for coordinating {t_clean} primitives?",
                "option_a": "Physical layer transmission cable",
                "option_b": "Control unit / Kernel scheduling and resource coordinator",
                "option_c": "Display monitor rasterizer",
                "option_d": "Power supply voltage inverter",
                "correct_option": "B",
                "explanation": "Control coordinators and system schedulers manage instruction pipelining and state distribution."
            },
            {
                "question_text": f"How does {t_clean} ensure fault isolation in distributed environments?",
                "option_a": "By using decoupled interfaces, write-ahead logs, and boundary checks.",
                "option_b": "By disabling network error-checking frames.",
                "option_c": "By executing all sub-tasks in a single unshared thread.",
                "option_d": "By skipping algorithmic verification.",
                "correct_option": "A",
                "explanation": "Decoupled architecture and persistent transaction logging isolate faults from cascading across peer nodes."
            }
        ]
        return templates[:count]

    def generate_flashcards(
        self,
        topic: str,
        count: int = 6,
        context_text: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Generates concise Front / Back flashcards for spaced repetition."""
        if self.ai.is_configured():
            try:
                prompt = f"""
Generate {count} educational flashcards for study topic: "{topic}".
Front: Core term or question.
Back: Concise, accurate academic definition or explanation (1-2 sentences).

Respond in JSON array format:
[
  {{ "front": "...", "back": "..." }}
]
Return only valid JSON.
"""
                resp = self.ai.client.models.generate_content(
                    model=self.ai.model_name,
                    contents=prompt
                )
                text = resp.text.strip()
                if text.startswith("```"):
                    text = re.sub(r"^```(?:json)?\s*", "", text)
                    text = re.sub(r"\s*```$", "", text)
                data = json.loads(text)
                return data[:count]
            except Exception as e:
                print(f"[QuizService] Flashcard generation via Gemini failed, using fallback: {e}")

        # Fallback flashcards
        t_clean = topic.strip()
        return [
            {
                "front": f"What is {t_clean}?",
                "back": f"A foundational mechanism that coordinates computational logic, ensures data integrity, and manages state transitions."
            },
            {
                "front": f"Core Advantage of {t_clean}",
                "back": "High operational throughput, predictable latency guarantees, and modular subsystem isolation."
            },
            {
                "front": f"Primary Limitation of {t_clean}",
                "back": "Requires rigorous synchronization protocols and introduces slight initial setup overhead."
            },
            {
                "front": f"Industry Application of {t_clean}",
                "back": "Widely deployed in distributed cloud services, operating system kernels, and database engines."
            },
            {
                "front": f"Crucial Invariant in {t_clean}",
                "back": "Internal state consistency must be verified and preserved across all lifecycle transitions."
            },
            {
                "front": f"Key Evaluation Metric for {t_clean}",
                "back": "Execution latency, computational space-time complexity, and fault tolerance resilience."
            }
        ][:count]
