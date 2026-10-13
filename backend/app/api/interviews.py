from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.interview import Interview
from app.schemas.interview import InterviewCreate, InterviewOut, InterviewDetailOut, InterviewResultOut
from app.schemas.answer import AnswerSubmit, AnswerOut, BatchAnswerSubmit
from app.services.auth_service import get_current_user
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/create", response_model=InterviewOut, status_code=status.HTTP_201_CREATED)
async def create_interview(
    interview_in: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interview = await InterviewService.create_interview(db, current_user, interview_in)
    return interview

@router.get("", response_model=List[InterviewOut])
def list_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).order_by(Interview.created_at.desc()).all()
    return interviews

@router.get("/{interview_id}", response_model=InterviewDetailOut)
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.get_interview_detail(db, interview_id, current_user)

@router.post("/{interview_id}/submit-answer", response_model=AnswerOut)
async def submit_answer(
    interview_id: int,
    answer_in: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await InterviewService.submit_answer(db, interview_id, current_user, answer_in)

@router.post("/{interview_id}/submit-batch")
async def submit_batch_answers(
    interview_id: int,
    batch_in: BatchAnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = []
    for ans in batch_in.answers:
        res = await InterviewService.submit_answer(db, interview_id, current_user, ans)
        results.append(res)
    completed = InterviewService.complete_interview(db, interview_id, current_user)
    return completed

@router.post("/{interview_id}/complete", response_model=InterviewResultOut)
def complete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.complete_interview(db, interview_id, current_user)

@router.get("/{interview_id}/results", response_model=InterviewResultOut)
def get_interview_results(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return InterviewService.get_interview_detail(db, interview_id, current_user)
