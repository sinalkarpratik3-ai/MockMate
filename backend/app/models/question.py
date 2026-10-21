from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    role = Column(String(100), nullable=False)
    round_number = Column(Integer, nullable=False, default=1)
    difficulty = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False, index=True)
    question_type = Column(String(20), nullable=False)  # "mcq" or "text"
    options = Column(Text, nullable=True)  # JSON-encoded string for MCQ options
    correct_option = Column(String(10), nullable=True)  # "A", "B", "C", "D"
    explanation = Column(Text, nullable=True)
    model_answer = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    interview = relationship("Interview", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="question", cascade="all, delete-orphan")
