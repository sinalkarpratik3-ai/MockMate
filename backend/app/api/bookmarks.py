from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.question import Question
from app.schemas.bookmark import BookmarkOut
from app.services.auth_service import get_current_user
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

@router.get("", response_model=List[Dict[str, Any]])
def get_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == current_user.id).order_by(Bookmark.created_at.desc()).all()
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
def add_bookmark(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")

    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()

    if existing:
        return {"message": "Question is already bookmarked.", "id": existing.id}

    bookmark = Bookmark(user_id=current_user.id, question_id=question_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return {"message": "Question successfully bookmarked.", "id": bookmark.id}

@router.delete("/{question_id}")
def remove_bookmark(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.question_id == question_id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found.")

    db.delete(bookmark)
    db.commit()
    return {"message": "Bookmark removed successfully."}
