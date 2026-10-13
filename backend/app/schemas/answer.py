from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: Optional[str] = None
    text_answer: Optional[str] = None

class AnswerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    interview_id: int
    question_id: int
    selected_option: Optional[str] = None
    text_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    score: float
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    missing_concepts: Optional[List[str]] = None
    improvement_tips: Optional[List[str]] = None
    model_answer: Optional[str] = None
    evaluated_at: datetime

class BatchAnswerSubmit(BaseModel):
    answers: List[AnswerSubmit]
