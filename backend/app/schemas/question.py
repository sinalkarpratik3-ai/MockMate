from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class MCQOption(BaseModel):
    key: str  # "A", "B", "C", "D"
    text: str

class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    interview_id: Optional[int] = None
    question_text: str
    role: str
    difficulty: str
    topic: str
    question_type: str  # "mcq" or "text"
    options: Optional[List[MCQOption]] = None
    created_at: datetime

class QuestionDetailOut(QuestionOut):
    correct_option: Optional[str] = None
    explanation: Optional[str] = None
    model_answer: Optional[str] = None
