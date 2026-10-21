import json
from datetime import date, datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.daily import DailyQuestion, DailyAttempt
from app.models.question import Question
from app.models.bookmark import Bookmark
from app.schemas.daily import DailyAttemptSubmit
from app.services.auth_service import get_current_user
from app.services.interview_service import InterviewService
from app.services.ai_service import ai_service, FALLBACK_MCQ_BANK

router = APIRouter(prefix="/daily", tags=["Question of the Day"])

async def _ensure_daily_question(db: AsyncSession) -> DailyQuestion:
    today = date.today()
    stmt = select(DailyQuestion).where(DailyQuestion.date == today)
    res = await db.execute(stmt)
    existing = res.scalar_one_or_none()
    if existing:
        return existing

    # Seed today's question based on day of year modulo roles
    roles = ["Frontend Developer", "Backend Developer", "Python Developer", "DevOps Engineer"]
    day_num = today.toordinal()
    selected_role = roles[day_num % len(roles)]
    diff_map = FALLBACK_MCQ_BANK.get(selected_role, FALLBACK_MCQ_BANK.get("Backend Developer", {}))
    role_questions = []
    for q_list in diff_map.values():
        if isinstance(q_list, list):
            role_questions.extend(q_list)
    if not role_questions:
        role_questions = [list(diff_map.values())[0][0]]
    q_data = role_questions[day_num % len(role_questions)]

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
    await db.commit()
    await db.refresh(new_daily)
    return new_daily

async def _ensure_daily_question_record(db: AsyncSession, daily_q: DailyQuestion) -> int:
    """Ensures a corresponding Question entity exists so the daily question can be bookmarked."""
    stmt = select(Question).where(Question.question_text == daily_q.question_text)
    res = await db.execute(stmt)
    q = res.scalar_one_or_none()
    if not q:
        q = Question(
            interview_id=None,
            question_text=daily_q.question_text,
            role=daily_q.role,
            round_number=1,
            difficulty=daily_q.difficulty,
            topic=daily_q.topic,
            question_type=daily_q.question_type,
            options=daily_q.options,
            correct_option=daily_q.correct_option,
            explanation=daily_q.explanation,
            model_answer=daily_q.model_answer
        )
        db.add(q)
        await db.commit()
        await db.refresh(q)
    return q.id

@router.get("", response_model=Dict[str, Any])
async def get_daily_question(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    daily_q = await _ensure_daily_question(db)
    q_id = await _ensure_daily_question_record(db, daily_q)

    att_stmt = select(DailyAttempt).where(
        DailyAttempt.user_id == current_user.id,
        DailyAttempt.daily_question_id == daily_q.id
    )
    att_res = await db.execute(att_stmt)
    attempt = att_res.scalar_one_or_none()

    # Check if currently bookmarked by user
    bm_stmt = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == q_id
    )
    bm_res = await db.execute(bm_stmt)
    is_bookmarked = bool(bm_res.scalar_one_or_none())

    opts = InterviewService._parse_options(daily_q.options) if daily_q.options else None

    response_data = {
        "id": daily_q.id,
        "question_id": q_id,
        "date": daily_q.date,
        "question_text": daily_q.question_text,
        "role": daily_q.role,
        "difficulty": daily_q.difficulty,
        "topic": daily_q.topic,
        "question_type": daily_q.question_type,
        "options": opts,
        "has_attempted": bool(attempt),
        "is_bookmarked": is_bookmarked,
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
    db: AsyncSession = Depends(get_db)
):
    daily_q = await _ensure_daily_question(db)
    att_stmt = select(DailyAttempt).where(
        DailyAttempt.user_id == current_user.id,
        DailyAttempt.daily_question_id == daily_q.id
    )
    att_res = await db.execute(att_stmt)
    existing = att_res.scalar_one_or_none()

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
    await db.commit()
    await db.refresh(attempt)

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
