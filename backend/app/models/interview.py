from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_role = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)
    mode = Column(String(20), nullable=False)  # "mcq" or "text"
    num_questions = Column(Integer, nullable=False, default=5)
    status = Column(String(30), nullable=False, default="in_progress")  # "in_progress", "completed"
    total_score = Column(Float, default=0.0)
    max_score = Column(Float, default=0.0)
    percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="interviews")
    questions = relationship("Question", back_populates="interview", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete-orphan")
