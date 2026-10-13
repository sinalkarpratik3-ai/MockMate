from datetime import datetime, timezone, date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.daily import DailyQuestion, DailyAttempt
from app.models.user import User

class AnalyticsService:
    @staticmethod
    def get_dashboard_summary(db: Session, user: User) -> Dict[str, Any]:
        # Completed interviews
        interviews_query = db.query(Interview).filter(
            Interview.user_id == user.id,
            Interview.status == "completed"
        ).order_by(Interview.completed_at.desc())
        
        completed_interviews = interviews_query.all()
        total_interviews = len(completed_interviews)

        # Questions attempted
        answers_query = db.query(Answer).filter(Answer.user_id == user.id)
        total_questions_attempted = answers_query.count()

        # MCQ accuracy
        mcq_answers = db.query(Answer).join(Interview).filter(
            Answer.user_id == user.id,
            Interview.mode == "mcq"
        ).all()
        if mcq_answers:
            correct_mcqs = sum(1 for a in mcq_answers if a.is_correct is True)
            mcq_accuracy_pct = round((correct_mcqs / len(mcq_answers)) * 100.0, 1)
        else:
            mcq_accuracy_pct = 0.0

        # Average text score (out of 10)
        text_answers = db.query(Answer).join(Interview).filter(
            Answer.user_id == user.id,
            Interview.mode == "text"
        ).all()
        if text_answers:
            avg_text_score = round(sum(a.score for a in text_answers) / len(text_answers), 1)
        else:
            avg_text_score = 0.0

        # Recent 5 interviews
        recent_interviews = [
            {
                "id": itv.id,
                "user_id": itv.user_id,
                "job_role": itv.job_role,
                "difficulty": itv.difficulty,
                "mode": itv.mode,
                "num_questions": itv.num_questions,
                "status": itv.status,
                "total_score": itv.total_score,
                "max_score": itv.max_score,
                "percentage": itv.percentage,
                "created_at": itv.created_at,
                "completed_at": itv.completed_at
            }
            for itv in completed_interviews[:5]
        ]

        # Weak topics identification
        weak_topics = AnalyticsService.get_weak_topics(db, user)

        # Role breakdown
        role_map: Dict[str, List[float]] = {}
        for itv in completed_interviews:
            role_map.setdefault(itv.job_role, []).append(itv.percentage)
        role_stats = [
            {
                "role": r,
                "interviews_count": len(scores),
                "avg_score_pct": round(sum(scores) / len(scores), 1)
            }
            for r, scores in role_map.items()
        ]

        # Difficulty breakdown
        diff_map: Dict[str, List[float]] = {}
        for itv in completed_interviews:
            diff_map.setdefault(itv.difficulty, []).append(itv.percentage)
        difficulty_stats = [
            {
                "difficulty": d,
                "count": len(scores),
                "avg_score_pct": round(sum(scores) / len(scores), 1)
            }
            for d, scores in diff_map.items()
        ]

        # Performance trends (chronological)
        performance_trends = [
            {
                "date": itv.completed_at.strftime("%Y-%m-%d %H:%M") if itv.completed_at else itv.created_at.strftime("%Y-%m-%d"),
                "score_percentage": itv.percentage,
                "mode": itv.mode,
                "role": itv.job_role
            }
            for itv in reversed(completed_interviews[:10])
        ]

        # Daily question status
        today = date.today()
        today_q = db.query(DailyQuestion).filter(DailyQuestion.date == today).first()
        has_attempted_daily = False
        if today_q:
            attempt = db.query(DailyAttempt).filter(
                DailyAttempt.user_id == user.id,
                DailyAttempt.daily_question_id == today_q.id
            ).first()
            has_attempted_daily = bool(attempt)

        return {
            "total_interviews": total_interviews,
            "total_questions_attempted": total_questions_attempted,
            "mcq_accuracy_pct": mcq_accuracy_pct,
            "avg_text_score": avg_text_score,
            "recent_interviews": recent_interviews,
            "weak_topics": weak_topics,
            "role_stats": role_stats,
            "difficulty_stats": difficulty_stats,
            "performance_trends": performance_trends,
            "has_attempted_daily": has_attempted_daily
        }

    @staticmethod
    def get_weak_topics(db: Session, user: User) -> List[Dict[str, Any]]:
        # Query answers grouped by question.topic and question.role
        answers_with_q = (
            db.query(Answer, Question)
            .join(Question, Answer.question_id == Question.id)
            .filter(Answer.user_id == user.id)
            .all()
        )

        topic_stats: Dict[str, Dict[str, Any]] = {}

        for ans, q in answers_with_q:
            key = f"{q.role}::{q.topic}"
            if key not in topic_stats:
                topic_stats[key] = {
                    "topic": q.topic,
                    "role": q.role,
                    "attempts": 0,
                    "total_score": 0.0,
                    "max_score": 0.0,
                    "correct_count": 0
                }
            ts = topic_stats[key]
            ts["attempts"] += 1
            if q.question_type == "mcq":
                ts["max_score"] += 1.0
                ts["total_score"] += (1.0 if ans.is_correct else 0.0)
                if ans.is_correct:
                    ts["correct_count"] += 1
            else:
                ts["max_score"] += 10.0
                ts["total_score"] += ans.score
                if ans.score >= 6.0:
                    ts["correct_count"] += 1

        weak_list = []
        for key, stat in topic_stats.items():
            if stat["max_score"] > 0:
                pct = (stat["total_score"] / stat["max_score"]) * 100.0
            else:
                pct = 0.0

            # Identify as weak if accuracy/score is under 60%
            if pct < 60.0:
                avg_score = round(stat["total_score"] / stat["attempts"], 1) if stat["attempts"] > 0 else 0.0
                weak_list.append({
                    "topic": stat["topic"],
                    "role": stat["role"],
                    "attempts": stat["attempts"],
                    "accuracy_percentage": round(pct, 1),
                    "avg_score": avg_score,
                    "recommendation": f"Focus revision on {stat['topic']} concepts for {stat['role']}."
                })

        # Sort from lowest accuracy first
        weak_list.sort(key=lambda x: x["accuracy_percentage"])
        return weak_list[:6]

analytics_service = AnalyticsService()
