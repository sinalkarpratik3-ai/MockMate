import json
from datetime import date, datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.daily import DailyQuestion, DailyAttempt
from app.schemas.daily import DailyQuestionOut, DailyAttemptSubmit, DailyAttemptOut
from app.services.auth_service import get_current_user
from app.services.interview_service import InterviewService
from app.services.ai_service import ai_service, FALLBACK_MCQ_BANK
from app.services.evaluation_service import evaluation_service

router = APIRouter(prefix="/daily", tags=["Question of the Day"])

def _ensure_daily_question(db: Session) -> DailyQuestion:
    today = date.today()
    existing = db.query(DailyQuestion).filter(DailyQuestion.date == today).first()
    if existing:
        return existing

    # Seed today's question based on day of year modulo roles
    roles = ["Frontend Developer", "Backend Developer", "Python Developer", "DevOps Engineer"]
    day_num = today.toordinal()
    selected_role = roles[day_num % len(roles)]
    bank = FALLBACK_MCQ_BANK.get(selected_role, FALLBACK_MCQ_BANK["Backend Developer"])
    q_data = bank[day_num % len(bank)]

    new_daily = DailyQuestion(
        date=today,
        question_text=q_data["question_text"],
        role=selected_role,
        difficulty="Mid-Level",
        topic=q_data["topic"],
        question_type="mcq",
        options=json.dumps(q_data["options"]),
        correct_option=q_data["correct_option"],
        explanation=q_data["explanation"],
        model_answer=None
    )
    db.add(new_daily)
    db.commit()
    db.refresh(new_daily)
    return new_daily

@router.get("", response_model=Dict[str, Any])
def get_daily_question(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    daily_q = _ensure_daily_question(db)
    attempt = db.query(DailyAttempt).filter(
        DailyAttempt.user_id == current_user.id,
        DailyAttempt.daily_question_id == daily_q.id
    ).first()

    opts = InterviewService._parse_options(daily_q.options) if daily_q.options else None

    response_data = {
        "id": daily_q.id,
        "date": daily_q.date,
        "question_text": daily_q.question_text,
        "role": daily_q.role,
        "difficulty": daily_q.difficulty,
        "topic": daily_q.topic,
        "question_type": daily_q.question_type,
        "options": opts,
        "has_attempted": bool(attempt),
        "user_attempt": None
    }

    if attempt:
        response_data["user_attempt"] = {
            "id": attempt.id,
            "submitted_answer": attempt.submitted_answer,
            "is_correct": attempt.is_correct,
            "score": attempt.score,
            "feedback": attempt.feedback,
            "correct_option": daily_q.correct_option,
            "explanation": daily_q.explanation,
            "model_answer": daily_q.model_answer,
            "created_at": attempt.created_at
        }

    return response_data

@router.post("/attempt", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def submit_daily_attempt(
    attempt_in: DailyAttemptSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    daily_q = _ensure_daily_question(db)
    existing = db.query(DailyAttempt).filter(
        DailyAttempt.user_id == current_user.id,
        DailyAttempt.daily_question_id == daily_q.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted an answer for today's Question of the Day."
        )

    ans_text = attempt_in.submitted_answer.strip()
    if daily_q.question_type == "mcq":
        is_correct = bool(ans_text.upper() == (daily_q.correct_option or "").upper())
        score = 10.0 if is_correct else 0.0
        feedback = "Correct! Well done." if is_correct else f"Incorrect. The correct answer was Option {daily_q.correct_option}."
    else:
        eval_result = await ai_service.evaluate_text_answer(
            role=daily_q.role,
            difficulty=daily_q.difficulty,
            question_text=daily_q.question_text,
            user_answer=ans_text,
            topic=daily_q.topic
        )
        score = eval_result["score"]
        is_correct = score >= 6.0
        feedback = eval_result["feedback"]

    attempt = DailyAttempt(
        user_id=current_user.id,
        daily_question_id=daily_q.id,
        submitted_answer=ans_text,
        is_correct=is_correct,
        score=score,
        feedback=feedback
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "id": attempt.id,
        "daily_question_id": daily_q.id,
        "submitted_answer": attempt.submitted_answer,
        "is_correct": attempt.is_correct,
        "score": attempt.score,
        "feedback": attempt.feedback,
        "correct_option": daily_q.correct_option,
        "explanation": daily_q.explanation,
        "model_answer": daily_q.model_answer,
        "created_at": attempt.created_at
    }
