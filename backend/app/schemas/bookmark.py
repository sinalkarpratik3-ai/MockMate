from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.question import QuestionDetailOut

class BookmarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    question_id: int
    created_at: datetime
    question: QuestionDetailOut
