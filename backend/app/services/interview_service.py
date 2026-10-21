import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.interview import Interview
from app.models.question import Question
from app.models.answer import Answer
from app.models.user import User
from app.schemas.interview import InterviewCreate
from app.schemas.answer import AnswerSubmit
from app.schemas.question import MCQOption
from app.services.ai_service import ai_service
from app.services.evaluation_service import evaluation_service
from app.services.question_banks import (
    DIFFICULTY_PROGRESSION,
    get_round_difficulty,
    adapt_difficulty,
    is_duplicate_or_near_duplicate,
    shuffle_mcq_options,
)

SUPPORTED_ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Web Developer",
    "Python Developer",
    "Java Developer",
    "Data Analyst",
    "Machine Learning Engineer",
    "Database Administrator",
    "Computer Networks",
    "DevOps Engineer",
    "Full Stack Developer",
    "Data Scientist",
    "Mobile Developer",
    "Software Engineer",
    "Cloud Architect",
    "Cybersecurity Analyst",
    "QA Engineer",
    "Go Developer",
    "Rust Developer",
    "Data Engineer",
    "Site Reliability Engineer",
    "Systems Engineer",
]

SUPPORTED_KEYWORDS = [
    "python", "java", "web", "frontend", "backend", "full stack", "fullstack",
    "data analyst", "machine learning", "deep learning", "database", "dba", "sql",
    "network", "networks", "devops", "cloud", "security", "docker", "kubernetes",
    "cybersecurity", "ai engineer", "mobile", "ios", "android", "software engineer",
    "data science", "data scientist", "qa", "test automation", "systems engineer",
    "go", "golang", "rust", "c++", "c#", ".net", "dotnet", "swift", "kotlin",
    "flutter", "react", "angular", "vue", "node", "typescript", "javascript",
    "data engineer", "sre", "site reliability", "embedded", "blockchain",
    "developer", "engineer", "architect", "analyst", "administrator", "programmer"
]

VALID_DIFFICULTIES = ["Junior", "Mid-Level", "Senior", "Easy", "Medium", "Hard"]
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
    async def create_interview(db: AsyncSession, user: User, interview_in: InterviewCreate) -> Interview:
        role = interview_in.job_role.strip()
        difficulty = interview_in.difficulty.strip()
        mode = interview_in.mode.strip().lower()

        # Validate that role belongs to supported technical domains or recognized keywords
        role_lower = role.lower()
        is_supported = (
            any(r.lower() == role_lower for r in SUPPORTED_ROLES) or
            any(kw in role_lower for kw in SUPPORTED_KEYWORDS)
        )
        if not role or len(role) < 2 or len(role) > 100 or not is_supported:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported domain or role '{role}'. Please select or specify a recognized technical domain (e.g. Python Developer, Machine Learning Engineer, Computer Networks, Database Administrator)."
            )

        if difficulty not in VALID_DIFFICULTIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty. Supported options: {', '.join(VALID_DIFFICULTIES)}"
            )

        if mode not in VALID_MODES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid mode. Choose 'mcq' or 'text'."
            )

        num_questions = min(max(interview_in.num_questions, 1), 10)

        # Query past questions for this user and domain to prevent repetition across sessions
        stmt = (
            select(Question.question_text)
            .join(Interview, Question.interview_id == Interview.id)
            .where(Interview.user_id == user.id, Interview.job_role.ilike(f"%{role}%"))
            .order_by(Question.id.desc())
            .limit(50)
        )
        res = await db.execute(stmt)
        recent_questions = [row[0] for row in res.all() if row[0]]

        # Generate questions with progressive difficulty (Round 1 is Easy, progressing to Hard)
        generated_questions = await ai_service.generate_questions(
            role=role,
            difficulty=difficulty,
            mode=mode,
            count=num_questions,
            exclude_questions=recent_questions,
            experience_level=difficulty
        )

        initial_diff = generated_questions[0]["difficulty"] if generated_questions else "Easy"

        db_interview = Interview(
            user_id=user.id,
            job_role=role,
            difficulty=difficulty,
            mode=mode,
            num_questions=len(generated_questions),
            current_round=1,
            current_difficulty=initial_diff,
            status="in_progress",
            max_score=float(len(generated_questions)) if mode == "mcq" else float(len(generated_questions) * 10.0)
        )
        db.add(db_interview)
        await db.flush()

        for idx, q_data in enumerate(generated_questions):
            assigned_round = q_data.get("round_number", idx + 1)
            assigned_diff = q_data.get("difficulty", get_round_difficulty(assigned_round, num_questions))

            raw_opts = q_data.get("options")
            raw_corr = q_data.get("correct_option")
            if mode == "mcq" and raw_opts:
                shuffled_opts, shuffled_key = shuffle_mcq_options(raw_opts, raw_corr)
                final_opts = json.dumps(shuffled_opts) if not isinstance(shuffled_opts, str) else shuffled_opts
                final_corr = shuffled_key
            else:
                final_opts = raw_opts
                final_corr = raw_corr

            db_question = Question(
                interview_id=db_interview.id,
                question_text=q_data["question_text"],
                role=role,
                round_number=assigned_round,
                difficulty=assigned_diff,
                topic=q_data["topic"],
                question_type=mode,
                options=final_opts,
                correct_option=final_corr,
                explanation=q_data.get("explanation"),
                model_answer=q_data.get("model_answer")
            )
            db.add(db_question)

        await db.commit()
        await db.refresh(db_interview)
        return db_interview

    @staticmethod
    async def get_interview_detail(db: AsyncSession, interview_id: int, user: User) -> Dict[str, Any]:
        stmt = select(Interview).where(Interview.id == interview_id)
        res = await db.execute(stmt)
        interview = res.scalar_one_or_none()

        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this interview.")

        q_stmt = select(Question).where(Question.interview_id == interview.id).order_by(Question.id.asc())
        q_res = await db.execute(q_stmt)
        questions = q_res.scalars().all()

        a_stmt = select(Answer).where(Answer.interview_id == interview.id)
        a_res = await db.execute(a_stmt)
        answers = a_res.scalars().all()

        questions_out = []
        is_completed = interview.status == "completed"

        for idx, q in enumerate(questions):
            opts = InterviewService._parse_options(q.options)
            assigned_round = getattr(q, "round_number", idx + 1) or (idx + 1)
            q_dict = {
                "id": q.id,
                "interview_id": q.interview_id,
                "question_text": q.question_text,
                "role": q.role,
                "round_number": assigned_round,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "question_type": q.question_type,
                "options": opts,
                "created_at": q.created_at
            }
            if is_completed:
                q_dict["correct_option"] = q.correct_option
                q_dict["explanation"] = q.explanation
                q_dict["model_answer"] = q.model_answer
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

        curr_round = getattr(interview, "current_round", 1) or 1
        curr_diff = getattr(interview, "current_difficulty", "Easy") or "Easy"

        return {
            "id": interview.id,
            "user_id": interview.user_id,
            "job_role": interview.job_role,
            "difficulty": interview.difficulty,
            "current_round": curr_round,
            "current_difficulty": curr_diff,
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
    async def submit_answer(db: AsyncSession, interview_id: int, user: User, answer_in: AnswerSubmit) -> Dict[str, Any]:
        stmt = select(Interview).where(Interview.id == interview_id)
        res = await db.execute(stmt)
        interview = res.scalar_one_or_none()

        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
        if interview.status == "completed":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Interview is already submitted.")

        q_stmt = select(Question).where(
            Question.id == answer_in.question_id,
            Question.interview_id == interview.id
        )
        q_res = await db.execute(q_stmt)
        question = q_res.scalar_one_or_none()

        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found in this interview.")

        # Evaluate based on mode
        if interview.mode == "mcq":
            eval_dict = evaluation_service.evaluate_mcq(question, answer_in.selected_option)
        else:
            eval_dict = await evaluation_service.evaluate_text(question, answer_in.text_answer)

        # Check existing answer
        ans_stmt = select(Answer).where(
            Answer.interview_id == interview.id,
            Answer.question_id == question.id
        )
        ans_res = await db.execute(ans_stmt)
        existing_answer = ans_res.scalar_one_or_none()

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

        # Adaptive Difficulty & Round Progression
        curr_round = getattr(question, "round_number", 1) or 1
        interview.current_round = min(curr_round + 1, interview.num_questions)

        # Calculate performance on this question
        perf_pct = 100.0 if ans.is_correct else (ans.score / 10.0 * 100.0 if interview.mode == "text" else 0.0)

        # Check subsequent unattempted questions in this session
        all_q_stmt = select(Question).where(Question.interview_id == interview.id).order_by(Question.id.asc())
        all_q_res = await db.execute(all_q_stmt)
        all_questions = all_q_res.scalars().all()

        ans_ids_stmt = select(Answer.question_id).where(Answer.interview_id == interview.id)
        ans_ids_res = await db.execute(ans_ids_stmt)
        answered_ids = set(ans_ids_res.scalars().all())
        answered_ids.add(question.id)

        unattempted = [q for q in all_questions if q.id not in answered_ids]
        if unattempted:
            next_q = unattempted[0]
            # Adapt next question's difficulty if struggling
            if perf_pct < 50.0 and next_q.difficulty in ["Hard", "Medium to Hard"]:
                next_q.difficulty = "Medium"
            elif perf_pct >= 80.0 and next_q.difficulty == "Easy":
                next_q.difficulty = "Easy to Medium"
            interview.current_difficulty = next_q.difficulty
        else:
            interview.current_difficulty = question.difficulty

        await db.commit()
        await db.refresh(ans)
        await db.refresh(interview)

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
    async def complete_interview(db: AsyncSession, interview_id: int, user: User) -> Dict[str, Any]:
        stmt = select(Interview).where(Interview.id == interview_id)
        res = await db.execute(stmt)
        interview = res.scalar_one_or_none()

        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found.")
        if interview.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

        q_stmt = select(Question).where(Question.interview_id == interview.id)
        q_res = await db.execute(q_stmt)
        questions = q_res.scalars().all()

        a_stmt = select(Answer).where(Answer.interview_id == interview.id)
        a_res = await db.execute(a_stmt)
        answers = list(a_res.scalars().all())

        # Automatically record unattempted answers for any skipped questions
        answered_q_ids = {a.question_id for a in answers}
        for q in questions:
            if q.id not in answered_q_ids:
                unattempted_ans = Answer(
                    interview_id=interview.id,
                    question_id=q.id,
                    user_id=user.id,
                    selected_option=None,
                    text_answer="",
                    is_correct=False,
                    score=0.0,
                    feedback="Question was not attempted during the practice session.",
                    strengths=json.dumps([]),
                    missing_concepts=json.dumps(["Question not attempted"]),
                    improvement_tips=json.dumps(["Review question explanation and sample answer"]),
                    model_answer=q.model_answer
                )
                db.add(unattempted_ans)
                answers.append(unattempted_ans)

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

        await db.commit()
        await db.refresh(interview)

        return await InterviewService.get_interview_detail(db, interview.id, user)
