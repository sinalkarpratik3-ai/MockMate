import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.user import User
from app.schemas.interview import InterviewCreate, InterviewResultOut
from app.schemas.answer import AnswerSubmit
from app.schemas.question import MCQOption, QuestionOut, QuestionDetailOut
from app.services.ai_service import ai_service
from app.services.evaluation_service import evaluation_service

VALID_ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Python Developer",
    "Java Developer",
    "DevOps Engineer",
    "Data Analyst"
]

VALID_DIFFICULTIES = ["Junior", "Mid-Level", "Senior"]
VALID_MODES = ["mcq", "text"]

class InterviewService:
    @staticmethod
    def _parse_options(options_json: Optional[str]) -> Optional[List[MCQOption]]:
        if not options_json:
            return None
        try:
            data = json.loads(options_json)
            if isinstance(data, list):
                return [MCQOption(key=opt.get("key", ""), text=opt.get("text", "")) for opt in data]
        except Exception:
            pass
        return None

    @staticmethod
    def _parse_json_list(text_json: Optional[str]) -> Optional[List[str]]:
        if not text_json:
            return None
        try:
            data = json.loads(text_json)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return None

    @staticmethod
    async def create_interview(db: Session, user: User, interview_in: InterviewCreate) -> Interview:
        role = interview_in.job_role.strip()
        difficulty = interview_in.difficulty.strip()
        mode = interview_in.mode.strip().lower()

        if role not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid job role. Supported roles: {', '.join(VALID_ROLES)}"
            )
        if difficulty not in VALID_DIFFICULTIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty. Supported difficulties: {', '.join(VALID_DIFFICULTIES)}"
            )
        if mode not in VALID_MODES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mode. Choose 'mcq' or 'text'."
            )

        num_questions = min(max(interview_in.num_questions, 1), 10)

        # Generate questions via AI Service (with robust fallback)
        generated_questions = await ai_service.generate_questions(
            role=role,
            difficulty=difficulty,
            mode=mode,
            count=num_questions
        )

        db_interview = Interview(
            user_id=user.id,
            job_role=role,
            difficulty=difficulty,
            mode=mode,
            num_questions=len(generated_questions),
            status="in_progress",
            max_score=len(generated_questions) if mode == "mcq" else len(generated_questions) * 10.0
        )
        db.add(db_interview)
        db.commit()
        db.refresh(db_interview)

        for q_data in generated_questions:
            db_question = Question(
                interview_id=db_interview.id,
                question_text=q_data["question_text"],
                role=role,
                difficulty=difficulty,
                topic=q_data["topic"],
                question_type=mode,
                options=q_data.get("options"),
                correct_option=q_data.get("correct_option"),
                explanation=q_data.get("explanation"),
                model_answer=q_data.get("model_answer")
            )
            db.add(db_question)

        db.commit()
        db.refresh(db_interview)
        return db_interview

    @staticmethod
    def get_interview_detail(db: Session, interview_id: int, user: User) -> Dict[str, Any]:
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this interview.")

        questions = db.query(Question).filter(Question.interview_id == interview.id).all()
        answers = db.query(Answer).filter(Answer.interview_id == interview.id).all()

        questions_out = []
        is_completed = interview.status == "completed"

        for q in questions:
            opts = InterviewService._parse_options(q.options)
            if is_completed:
                q_dict = {
                    "id": q.id,
                    "interview_id": q.interview_id,
                    "question_text": q.question_text,
                    "role": q.role,
                    "difficulty": q.difficulty,
                    "topic": q.topic,
                    "question_type": q.question_type,
                    "options": opts,
                    "correct_option": q.correct_option,
                    "explanation": q.explanation,
                    "model_answer": q.model_answer,
                    "created_at": q.created_at
                }
            else:
                q_dict = {
                    "id": q.id,
                    "interview_id": q.interview_id,
                    "question_text": q.question_text,
                    "role": q.role,
                    "difficulty": q.difficulty,
                    "topic": q.topic,
                    "question_type": q.question_type,
                    "options": opts,
                    "created_at": q.created_at
                }
            questions_out.append(q_dict)

        answers_out = []
        for a in answers:
            answers_out.append({
                "id": a.id,
                "interview_id": a.interview_id,
                "question_id": a.question_id,
                "selected_option": a.selected_option,
                "text_answer": a.text_answer,
                "is_correct": a.is_correct,
                "score": a.score,
                "feedback": a.feedback,
                "strengths": InterviewService._parse_json_list(a.strengths),
                "missing_concepts": InterviewService._parse_json_list(a.missing_concepts),
                "improvement_tips": InterviewService._parse_json_list(a.improvement_tips),
                "model_answer": a.model_answer if is_completed else None,
                "evaluated_at": a.evaluated_at
            })

        return {
            "id": interview.id,
            "user_id": interview.user_id,
            "job_role": interview.job_role,
            "difficulty": interview.difficulty,
            "mode": interview.mode,
            "num_questions": interview.num_questions,
            "status": interview.status,
            "total_score": interview.total_score,
            "max_score": interview.max_score,
            "percentage": interview.percentage,
            "created_at": interview.created_at,
            "completed_at": interview.completed_at,
            "questions": questions_out,
            "answers": answers_out
        }

    @staticmethod
    async def submit_answer(db: Session, interview_id: int, user: User, answer_in: AnswerSubmit) -> Dict[str, Any]:
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
        if interview.status == "completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview is already submitted.")

        question = db.query(Question).filter(
            Question.id == answer_in.question_id,
            Question.interview_id == interview.id
        ).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found in this interview.")

        # Evaluate based on mode
        if interview.mode == "mcq":
            eval_dict = evaluation_service.evaluate_mcq(question, answer_in.selected_option)
        else:
            eval_dict = await evaluation_service.evaluate_text(question, answer_in.text_answer)

        # Check existing answer
        existing_answer = db.query(Answer).filter(
            Answer.interview_id == interview.id,
            Answer.question_id == question.id
        ).first()

        if existing_answer:
            existing_answer.selected_option = eval_dict["selected_option"]
            existing_answer.text_answer = eval_dict["text_answer"]
            existing_answer.is_correct = eval_dict["is_correct"]
            existing_answer.score = eval_dict["score"]
            existing_answer.feedback = eval_dict["feedback"]
            existing_answer.strengths = eval_dict["strengths"]
            existing_answer.missing_concepts = eval_dict["missing_concepts"]
            existing_answer.improvement_tips = eval_dict["improvement_tips"]
            existing_answer.model_answer = eval_dict["model_answer"]
            existing_answer.evaluated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(existing_answer)
            ans = existing_answer
        else:
            ans = Answer(
                interview_id=interview.id,
                question_id=question.id,
                user_id=user.id,
                selected_option=eval_dict["selected_option"],
                text_answer=eval_dict["text_answer"],
                is_correct=eval_dict["is_correct"],
                score=eval_dict["score"],
                feedback=eval_dict["feedback"],
                strengths=eval_dict["strengths"],
                missing_concepts=eval_dict["missing_concepts"],
                improvement_tips=eval_dict["improvement_tips"],
                model_answer=eval_dict["model_answer"]
            )
            db.add(ans)
            db.commit()
            db.refresh(ans)

        return {
            "id": ans.id,
            "interview_id": ans.interview_id,
            "question_id": ans.question_id,
            "selected_option": ans.selected_option,
            "text_answer": ans.text_answer,
            "is_correct": ans.is_correct,
            "score": ans.score,
            "feedback": ans.feedback,
            "strengths": InterviewService._parse_json_list(ans.strengths),
            "missing_concepts": InterviewService._parse_json_list(ans.missing_concepts),
            "improvement_tips": InterviewService._parse_json_list(ans.improvement_tips),
            "model_answer": ans.model_answer if interview.status == "completed" else None,
            "evaluated_at": ans.evaluated_at
        }

    @staticmethod
    def complete_interview(db: Session, interview_id: int, user: User) -> Dict[str, Any]:
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

        questions = db.query(Question).filter(Question.interview_id == interview.id).all()
        answers = db.query(Answer).filter(Answer.interview_id == interview.id).all()

        total_score = sum(a.score for a in answers)
        if interview.mode == "mcq":
            max_score = float(len(questions))
        else:
            max_score = float(len(questions) * 10.0)

        percentage = (total_score / max_score * 100.0) if max_score > 0 else 0.0

        interview.total_score = total_score
        interview.max_score = max_score
        interview.percentage = round(percentage, 1)
        interview.status = "completed"
        interview.completed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(interview)

        return InterviewService.get_interview_detail(db, interview.id, user)
