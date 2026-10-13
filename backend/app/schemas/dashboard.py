from pydantic import BaseModel
from typing import List, Optional
from app.schemas.interview import InterviewOut

class WeakTopicItem(BaseModel):
    topic: str
    role: str
    attempts: int
    accuracy_percentage: float
    avg_score: float
    recommendation: str

class RoleStats(BaseModel):
    role: str
    interviews_count: int
    avg_score_pct: float

class DifficultyStats(BaseModel):
    difficulty: str
    count: int
    avg_score_pct: float

class PerformanceTrendPoint(BaseModel):
    date: str
    score_percentage: float
    mode: str
    role: str

class DashboardSummary(BaseModel):
    total_interviews: int
    total_questions_attempted: int
    mcq_accuracy_pct: float
    avg_text_score: float  # out of 10.0
    recent_interviews: List[InterviewOut] = []
    weak_topics: List[WeakTopicItem] = []
    role_stats: List[RoleStats] = []
    difficulty_stats: List[DifficultyStats] = []
    performance_trends: List[PerformanceTrendPoint] = []
    has_attempted_daily: bool = False
