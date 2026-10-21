from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_option = Column(String(10), nullable=True)
    text_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, default=0.0)
    feedback = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)         # JSON list string
    missing_concepts = Column(Text, nullable=True)  # JSON list string
    improvement_tips = Column(Text, nullable=True)  # JSON list string
    model_answer = Column(Text, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    interview = relationship("Interview", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")
