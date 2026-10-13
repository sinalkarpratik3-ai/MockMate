import json
from typing import Dict, Any, Optional
from app.models.question import Question
from app.services.ai_service import ai_service

class EvaluationService:
    @staticmethod
    def evaluate_mcq(question: Question, selected_option: Optional[str]) -> Dict[str, Any]:
        """Evaluates an MCQ answer deterministically without unnecessary AI latency."""
        selected_clean = (selected_option or "").strip().upper()
        correct_clean = (question.correct_option or "").strip().upper()

        is_correct = bool(selected_clean and selected_clean == correct_clean)
        score = 1.0 if is_correct else 0.0

        if is_correct:
            feedback = f"Correct! Option {correct_clean} is the right answer."
        else:
            feedback = f"Incorrect. The correct answer is Option {correct_clean}."

        return {
            "selected_option": selected_clean,
            "text_answer": None,
            "is_correct": is_correct,
            "score": score,
            "feedback": feedback,
            "strengths": json.dumps(["Selected the correct option"]) if is_correct else json.dumps([]),
            "missing_concepts": json.dumps([]) if is_correct else json.dumps(["Core concept testing"]),
            "improvement_tips": json.dumps([]) if is_correct else json.dumps(["Review question explanation and related concepts"]),
            "model_answer": None
        }

    @staticmethod
    async def evaluate_text(question: Question, user_text: Optional[str]) -> Dict[str, Any]:
        """Evaluates a text-based technical response using Google Gemini."""
        text_clean = (user_text or "").strip()
        if not text_clean:
            return {
                "selected_option": None,
                "text_answer": "",
                "is_correct": False,
                "score": 0.0,
                "feedback": "No answer was submitted.",
                "strengths": json.dumps([]),
                "missing_concepts": json.dumps(["Entire question was unanswered"]),
                "improvement_tips": json.dumps(["Always attempt to provide key conceptual terms"]),
                "model_answer": question.model_answer or "Comprehensive technical explanation required."
            }

        eval_result = await ai_service.evaluate_text_answer(
            role=question.role,
            difficulty=question.difficulty,
            question_text=question.question_text,
            user_answer=text_clean,
            topic=question.topic
        )

        score = float(eval_result.get("score", 5.0))
        is_correct = score >= 6.0

        return {
            "selected_option": None,
            "text_answer": text_clean,
            "is_correct": is_correct,
            "score": score,
            "feedback": eval_result.get("feedback", ""),
            "strengths": json.dumps(eval_result.get("strengths", [])),
            "missing_concepts": json.dumps(eval_result.get("missing_concepts", [])),
            "improvement_tips": json.dumps(eval_result.get("improvement_tips", [])),
            "model_answer": eval_result.get("model_answer", question.model_answer)
        }

evaluation_service = EvaluationService()
