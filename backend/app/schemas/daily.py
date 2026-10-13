from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from app.schemas.question import MCQOption

class DailyQuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: date
    question_text: str
    role: str
    difficulty: str
    topic: str
    question_type: str
    options: Optional[List[MCQOption]] = None
    has_attempted: bool = False
    user_attempt: Optional[dict] = None

class DailyAttemptSubmit(BaseModel):
    submitted_answer: str

class DailyAttemptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    daily_question_id: int
    submitted_answer: str
    is_correct: Optional[bool] = None
    score: float
    feedback: Optional[str] = None
    correct_option: Optional[str] = None
    explanation: Optional[str] = None
    model_answer: Optional[str] = None
    created_at: datetime
