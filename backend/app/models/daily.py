from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class DailyQuestion(Base):
    __tablename__ = "daily_questions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True, nullable=False)
    question_text = Column(Text, nullable=False)
    role = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False)
    question_type = Column(String(20), nullable=False)  # "mcq" or "text"
    options = Column(Text, nullable=True)               # JSON options for MCQ
    correct_option = Column(String(10), nullable=True)
    explanation = Column(Text, nullable=True)
    model_answer = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    attempts = relationship("DailyAttempt", back_populates="daily_question", cascade="all, delete-orphan")

class DailyAttempt(Base):
    __tablename__ = "daily_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    daily_question_id = Column(Integer, ForeignKey("daily_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, default=0.0)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("user_id", "daily_question_id", name="uq_user_daily_attempt"),
    )

    user = relationship("User", back_populates="daily_attempts")
    daily_question = relationship("DailyQuestion", back_populates="attempts")
