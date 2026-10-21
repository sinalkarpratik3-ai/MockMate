from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.question import QuestionOut, QuestionDetailOut
from app.schemas.answer import AnswerOut

class InterviewCreate(BaseModel):
    job_role: str = Field(..., description="Target job role")
    difficulty: str = Field(..., description="Junior, Mid-Level, or Senior")
    mode: str = Field(..., description="'mcq' or 'text'")
    num_questions: int = Field(5, ge=1, le=10, description="Number of questions (1-10)")

class InterviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    job_role: str
    difficulty: str
    mode: str
    num_questions: int
    current_round: Optional[int] = 1
    current_difficulty: Optional[str] = "Easy"
    status: str
    total_score: float
    max_score: float
    percentage: float
    created_at: datetime
    completed_at: Optional[datetime] = None

class InterviewDetailOut(InterviewOut):
    questions: List[QuestionOut] = []
    answers: List[AnswerOut] = []

class InterviewResultOut(InterviewOut):
    questions: List[QuestionDetailOut] = []
    answers: List[AnswerOut] = []
    summary_feedback: Optional[str] = None
