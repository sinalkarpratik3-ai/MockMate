from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.question import Question
from app.services.auth_service import get_current_user
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

@router.get("", response_model=List[Dict[str, Any]])
async def get_bookmarks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Bookmark)
        .options(selectinload(Bookmark.question))
        .where(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at.desc())
    )
    result = await db.execute(stmt)
    bookmarks = result.scalars().all()

    out = []
    for b in bookmarks:
        q = b.question
        opts = InterviewService._parse_options(q.options) if q.options else None
        out.append({
            "id": b.id,
            "user_id": b.user_id,
            "question_id": b.question_id,
            "created_at": b.created_at,
            "question": {
                "id": q.id,
                "interview_id": q.interview_id,
                "question_text": q.question_text,
                "role": q.role,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "question_type": q.question_type,
                "options": opts,
                "correct_option": q.correct_option,
                "explanation": q.explanation,
                "model_answer": q.model_answer,
                "created_at": q.created_at
            }
        })
    return out

@router.post("/{question_id}", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    q_stmt = select(Question).where(Question.id == question_id)
    q_res = await db.execute(q_stmt)
    question = q_res.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")

    b_stmt = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    )
    b_res = await db.execute(b_stmt)
    existing = b_res.scalar_one_or_none()

    if existing:
        return {"message": "Question is already bookmarked.", "id": existing.id}

    bookmark = Bookmark(user_id=current_user.id, question_id=question_id)
    db.add(bookmark)
    await db.commit()
    await db.refresh(bookmark)
    return {"message": "Question successfully bookmarked.", "id": bookmark.id}

@router.delete("/{question_id}")
async def remove_bookmark(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    b_stmt = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    )
    b_res = await db.execute(b_stmt)
    bookmark = b_res.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found.")

    await db.delete(bookmark)
    await db.commit()
    return {"message": "Bookmark removed successfully."}
