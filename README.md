# MockMate: AI-Based Interview Preparation Simulator

![MockMate Banner](https://img.shields.io/badge/MockMate-AI%20Interview%20Simulator-4F46E5?style=for-the-badge&logo=fastapi&logoColor=white)
![Build Status](https://img.shields.io/badge/Tests-12%2F12%20Passing-emerald?style=for-the-badge)
![Render Ready](https://img.shields.io/badge/Render-Deployment%20Ready-46E3B7?style=for-the-badge&logo=render)

---

## 1. Project Title
**MockMate: AI-Based Interview Preparation Simulator**

---

## 2. Project Overview
MockMate is an enterprise-grade, end-to-end web application engineered to bridge the gap between technical interview anxiety and confident performance. By integrating the Google Gemini API with deterministic evaluation pipelines and persistent PostgreSQL telemetry, MockMate simulates real-world engineering interviews across multiple job roles, difficulties, and practice modes.

Candidates can practice rapid-fire multiple-choice questions (MCQs), submit in-depth architectural written answers evaluated against a 6-point technical rubric, view ideal model answers, track their performance trajectory over time, practice a daily featured challenge, and systematically eliminate their weak topics.

---

## 3. Problem Statement
Technical interview preparation is traditionally fragmented and inefficient:
- Static question banks quickly become repetitive, lack role-specific calibration, and do not test deep practical trade-offs.
- Practicing coding problems alone does not prepare engineers for conceptual, architectural, or behavioral interview questions.
- Peer mock interviews are difficult to schedule, inconsistent in feedback quality, and lack objective historical performance tracking.
- Candidates lack clear diagnostic data identifying which exact technical concepts are consistently pulling down their scores.

---

## 4. Project Objectives
1. Provide a reliable, AI-driven technical interview simulator that generates tailored questions dynamically.
2. Deliver dual assessment modes: fast deterministic MCQ practice and in-depth written answer evaluations.
3. Eliminate guesswork with instant scoring, feedback bullets, missing keyword detection, and authoritative model answers.
4. Persist all user attempts, scores, and sessions in a production-ready database (PostgreSQL).
5. Compute real-time analytics to highlight weak topics (&lt;60% accuracy) and offer 1-click targeted revision.
6. Build a Question of the Day streak feature to foster daily preparation habits.
7. Ensure 100% Render hosting compatibility and strict security with password hashing and JWT isolation.

---

## 5. Project Scope
The approved project scope encompasses exactly 13 core functional modules:
- **Module 1**: User Authentication & Session Security
- **Module 2**: Personalized Interview Preparation
- **Module 3**: Multiple Answer Modes (MCQ & Text)
- **Module 4**: AI-Powered Question Generation (Google Gemini)
- **Module 5**: Automated Answer Evaluation (Deterministic MCQ + AI Rubric)
- **Module 6**: Instant Feedback & Scorecard Display
- **Module 7**: Engineering Model Answers
- **Module 8**: Progress Tracking & Aggregated Telemetry
- **Module 9**: Weak Topic Identification & Recommendation Engine
- **Module 10**: Interview History & Question Bookmarks
- **Module 11**: Question of the Day
- **Module 12**: Performance Analytics Dashboard
- **Module 13**: Responsive SaaS UI/UX adhering to Shneiderman's 8 Golden Rules

---

## 6. Key Features
- **Dynamic Question Generation**: Context-aware prompts requesting structured JSON questions for the candidate's exact role and difficulty tier.
- **Dual Assessment Engine**: Deterministic instant evaluation for MCQs; 6-criterion rubric evaluation (technical depth, correctness, clarity, completeness, missing keywords) for text answers.
- **Weak Topic Auto-Detection**: Flags concepts where performance falls below 60% across attempted sessions.
- **Question Bookmarks Notebook**: Save challenging questions with full model answers and explanations to revise later.
- **Daily Practice Streak**: One daily technical challenge per calendar day with duplicate attempt prevention.
- **Private Data Isolation**: JWT-secured endpoints ensure users can only ever view and edit their own private sessions.
- **Offline / Quota Resilience Engine**: Integrated domain fallback generator ensures 100% uptime even if API quotas fluctuate.

---

## 7. MCQ and Text-Based Interview Modes

### Mode A: MCQ-Based Interview
- **Format**: 4 distinct options (A, B, C, D) per question.
- **Correctness Guard**: Correct answers and explanations are hidden during an active test to guarantee honesty.
- **Evaluation**: Deterministic server-side evaluation (`is_correct = (selected == correct_option)`). Zero AI hallucination or latency.
- **Navigation**: Previous/Next buttons, question jump palette, progress indicator, and final review confirmation modal.
- **Post-Submission**: Detailed breakdown showing your choice, the correct option, correct/incorrect status badge, and comprehensive technical explanation.

### Mode B: Text-Based Technical Interview
- **Format**: Multiline text editor supporting architectural explanations and code snippets.
- **Evaluation**: Sent to Google Gemini API and evaluated across 6 criteria:
  1. Technical correctness
  2. Relevance to question
  3. Conceptual depth
  4. Clarity & organization
  5. Completeness
  6. Missing technical keywords
- **Output**: Integer score (0 to 10), bulleted strengths, missing concepts, actionable advice, and an ideal engineering model answer.

---

## 8. Functional Modules
```
[User Auth] ──> [Configuration] ──> [AI Question Generator] ──> [Workspace (MCQ/Text)]
     │                                                                 │
     ▼                                                                 ▼
[Dashboard] <── [Analytics Engine] <── [DB Persistence] <── [Evaluation Engine]
     │
     ├──> [Question of the Day]
     ├──> [Saved Questions Notebook]
     └──> [Weak Topics Recommender]
```

---

## 9. Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router, Turbopack, React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Icons**: Lucide React
- **Architecture**: Modular components, React Context state management, custom API fetch client.

### Backend
- **Framework**: Python FastAPI
- **Data Validation**: Pydantic v2 & Pydantic-Settings
- **ORM & Database**: SQLAlchemy 2.0 (PostgreSQL in production, SQLite for local testing)
- **Security**: Native Bcrypt password hashing, Python-Jose (JWT HS256 tokens)
- **AI Integration**: Google Gemini API via asynchronous `httpx` with JSON schema enforcement.
- **Testing**: Pytest & Pytest-Asyncio

---

## 10. System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                       │
│     (Landing, Dashboard, Workspace, Results, Bookmarks)     │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / JSON (REST API)
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Backend Service                  │
│  ┌─────────────────┬───────────────────┬─────────────────┐  │
│  │ Auth & Security │ Interview Service │ Analytics Engine│  │
│  └────────┬────────┴─────────┬─────────┴────────┬────────┘  │
└───────────┼──────────────────┼──────────────────┼───────────┘
            │                  │                  │
            ▼                  ▼                  ▼
   ┌─────────────────┐ ┌───────────────┐ ┌────────────────┐
   │   PostgreSQL    │ │ Google Gemini │ │ Heuristic Fall-│
   │    Database     │ │    API (LLM)  │ │   back Engine  │
   └─────────────────┘ └───────────────┘ └────────────────┘
```

---

## 11. Project Directory Structure
```text
MockMate/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Register, login, me
│   │   │   ├── interviews.py    # Create, answer, complete, results
│   │   │   ├── bookmarks.py     # List, add, remove saved questions
│   │   │   ├── daily.py         # Question of the Day & attempts
│   │   │   ├── dashboard.py     # Aggregated telemetry & KPIs
│   │   │   └── health.py        # System health & DB heartbeat
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic BaseSettings
│   │   │   ├── database.py      # SQLAlchemy engine & sessionmaker
│   │   │   └── security.py      # Bcrypt hash & JWT encode/decode
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # Users table
│   │   │   ├── interview.py     # Interviews table
│   │   │   ├── question.py      # Questions table
│   │   │   ├── answer.py        # Evaluated answers table
│   │   │   ├── bookmark.py      # Saved questions table
│   │   │   └── daily.py         # DailyQuestions & DailyAttempts tables
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Request & response Pydantic models
│   │   │   ├── interview.py
│   │   │   ├── question.py
│   │   │   ├── answer.py
│   │   │   ├── bookmark.py
│   │   │   ├── daily.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── auth_service.py       # Authentication logic
│   │   │   ├── ai_service.py         # Google Gemini integration & fallbacks
│   │   │   ├── interview_service.py  # Session lifecycle
│   │   │   ├── evaluation_service.py # MCQ & Text scoring logic
│   │   │   └── analytics_service.py  # KPI aggregation & weak topics
│   │   └── main.py              # FastAPI application entrypoint
│   ├── tests/
│   │   ├── conftest.py          # Pytest fixtures & in-memory test DB
│   │   ├── test_auth.py         # 6 authentication test cases
│   │   └── test_interviews.py   # 6 interview & analytics test cases
│   └── requirements.txt         # Backend Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout & AuthProvider
│   │   │   ├── page.tsx         # Landing page
│   │   │   ├── login/page.tsx   # Login page
│   │   │   ├── register/page.tsx# Registration page
│   │   │   ├── dashboard/page.tsx   # Main Dashboard
│   │   │   ├── interviews/
│   │   │   │   ├── new/page.tsx     # Configuration page
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx     # Active Workspace
│   │   │   │       └── results/page.tsx # Scorecard & Review
│   │   │   ├── history/page.tsx     # History list
│   │   │   ├── bookmarks/page.tsx   # Saved Questions
│   │   │   ├── daily/page.tsx       # Question of the Day
│   │   │   ├── analytics/page.tsx   # Progress Analytics
│   │   │   └── profile/page.tsx     # Profile & Settings
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Navigation bar
│   │   │   ├── Sidebar.tsx      # Responsive desktop/mobile sidebar
│   │   │   └── AppLayout.tsx    # Auth guard & unified layout
│   │   ├── context/
│   │   │   └── AuthContext.tsx  # User state & JWT persistence
│   │   ├── lib/
│   │   │   └── api.ts           # Fetch API client with Bearer headers
│   │   └── types/
│   │       └── index.ts         # TypeScript entity definitions
│   ├── package.json
│   └── tsconfig.json
│
├── render.yaml                  # Render Blueprint deployment definition
├── .env.example                 # Environment variables reference
├── .gitignore
└── README.md
```

---

## 12. Application Workflow
1. **Registration / Login**: User creates an account; credentials hashed via Bcrypt; JWT token returned and stored in localStorage.
2. **Configuration**: User chooses Role, Difficulty, Mode (MCQ or Text), and Question count (3, 5, or 10).
3. **Session Creation**: Backend validates configuration, queries Gemini API for structured JSON questions, and persists an in-progress session.
4. **Active Workspace**: User answers questions, navigates using the question palette, and submits answers.
5. **Evaluation**:
   - For MCQ: Deterministic server-side evaluation.
   - For Text: Gemini evaluates depth, correctness, missing concepts, tips, and model answer.
6. **Scorecard**: Complete interview finalized; percentage calculated; answers, explanations, and model answers unlocked.
7. **Telemetry & Revision**: Dashboard metrics, role breakdowns, and weak topics automatically update; candidate bookmarks difficult questions.

---

## 13. Database Schema and Relationships
- **users**: `id (PK)`, `email (Unique)`, `hashed_password`, `full_name`, `created_at`, `updated_at`.
- **interviews**: `id (PK)`, `user_id (FK -> users.id)`, `job_role`, `difficulty`, `mode`, `num_questions`, `status`, `total_score`, `max_score`, `percentage`, `created_at`, `completed_at`.
- **questions**: `id (PK)`, `interview_id (FK -> interviews.id)`, `question_text`, `role`, `difficulty`, `topic`, `question_type`, `options (JSON)`, `correct_option`, `explanation`, `model_answer`, `created_at`.
- **answers**: `id (PK)`, `interview_id (FK -> interviews.id)`, `question_id (FK -> questions.id)`, `user_id (FK -> users.id)`, `selected_option`, `text_answer`, `is_correct`, `score`, `feedback`, `strengths (JSON)`, `missing_concepts (JSON)`, `improvement_tips (JSON)`, `model_answer`, `evaluated_at`.
- **bookmarks**: `id (PK)`, `user_id (FK -> users.id)`, `question_id (FK -> questions.id)`, `created_at`, `UniqueConstraint(user_id, question_id)`.
- **daily_questions**: `id (PK)`, `date (Unique Date)`, `question_text`, `role`, `difficulty`, `topic`, `question_type`, `options (JSON)`, `correct_option`, `explanation`, `model_answer`, `created_at`.
- **daily_attempts**: `id (PK)`, `user_id (FK -> users.id)`, `daily_question_id (FK -> daily_questions.id)`, `submitted_answer`, `is_correct`, `score`, `feedback`, `created_at`, `UniqueConstraint(user_id, daily_question_id)`.

---

## 14. API Endpoint Documentation

### Authentication
- `POST /api/auth/register` — Register a new account.
- `POST /api/auth/login` — Authenticate and receive JWT access token.
- `POST /api/auth/logout` — Invalidate client session.
- `GET /api/auth/me` — Retrieve current authenticated user profile.

### Interview Management
- `POST /api/interviews/create` — Configure and start a new interview session.
- `GET /api/interviews` — List all interview sessions for authenticated user.
- `GET /api/interviews/{id}` — Get active or completed interview session details.
- `POST /api/interviews/{id}/submit-answer` — Submit single question answer.
- `POST /api/interviews/{id}/submit-batch` — Submit all answers and complete session.
- `POST /api/interviews/{id}/complete` — Finalize score and mark session completed.
- `GET /api/interviews/{id}/results` — Get full scorecard and explanations.

### Bookmarks
- `GET /api/bookmarks` — List all bookmarked questions for user.
- `POST /api/bookmarks/{question_id}` — Save question to revision notebook.
- `DELETE /api/bookmarks/{question_id}` — Remove question from bookmarks.

### Question of the Day
- `GET /api/daily` — Fetch today's featured question.
- `POST /api/daily/attempt` — Submit today's answer (locks after 1 attempt).

### Dashboard & Analytics
- `GET /api/dashboard` — Fetch KPI summaries, role stats, weak topics, and trends.

### System Health
- `GET /api/health` — Service and database connection heartbeat.

---

## 15. Prerequisites
- **Python**: 3.10, 3.11, 3.12, 3.13, or 3.14
- **Node.js**: v18+, v20+ (LTS recommended)
- **Package Managers**: `pip` and `npm`
- **PostgreSQL**: Optional locally (defaults to SQLite if PostgreSQL not running; PostgreSQL used in Render production).

---

## 16. Local Installation Instructions
Clone the repository:
```bash
git clone https://github.com/sinalkarpratik3-ai/MockMate.git
cd MockMate
```

---

## 17. Frontend Setup
```bash
cd frontend
npm install
```

Configure `.env.local` inside `frontend/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## 18. Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 19. PostgreSQL Setup
For local PostgreSQL (optional):
```sql
CREATE DATABASE mockmate;
CREATE USER mockmate_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE mockmate TO mockmate_user;
```
Update `DATABASE_URL` in `backend/.env`:
```env
DATABASE_URL=postgresql://mockmate_user:secure_password@localhost:5432/mockmate
```
*(If omitted, MockMate automatically defaults to local SQLite `sqlite:///./mockmate.db`).*

---

## 20. Gemini API Configuration
1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Add your key to `backend/.env`:
```env
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
GEMINI_MODEL=gemini-1.5-flash
```
*(If no key is provided, MockMate runs seamlessly using its built-in verified engineering question generator).*

---

## 21. Environment Variable Reference
| Variable | Required | Description | Default |
|---|---|---|---|
| `DATABASE_URL` | No | PostgreSQL / SQLite connection string | `sqlite:///./mockmate.db` |
| `SECRET_KEY` | Yes (in prod) | Secret key for JWT hashing | `super-secret-jwt-key` |
| `GEMINI_API_KEY` | Optional | Google Gemini API Key | `""` |
| `GEMINI_MODEL` | No | Gemini model name | `gemini-1.5-flash` |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL for frontend | `http://localhost:8000/api` |

---

## 22. Database Migration Instructions
Database tables are automatically created on backend startup via SQLAlchemy lifespan hooks (`Base.metadata.create_all(bind=engine)`).

For Alembic migrations:
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

## 23. How to Run the Application Locally

### Start Backend
```bash
cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API runs at: `http://127.0.0.1:8000` (Swagger docs at `http://127.0.0.1:8000/api/docs`).

### Start Frontend
```bash
cd frontend
npm run dev
```
Web app runs at: `http://localhost:3000`.

---

## 24. How to Run Tests
MockMate includes 12 automated unit and integration tests covering Authentication, Interview Lifecycle, MCQ Deterministic Scoring, Text Rubric Evaluation, Bookmarks, and Analytics Isolation.

```bash
cd backend
.venv\Scripts\Activate.ps1
pytest tests -v
```

Expected output:
```text
======================= 12 passed in 9.91s ========================
```

---

## 25. GitHub Workflow
1. Check repository status:
   ```bash
   git status
   ```
2. Add modified files and commit:
   ```bash
   git add .
   git commit -m "feat: complete AI interview preparation simulator implementation"
   ```
3. Push to your repository:
   ```bash
   git push origin main
   ```

---

## 26. Render Deployment Guide

### Deploying via Render Blueprint (`render.yaml`):
1. Push your code to GitHub at `https://github.com/sinalkarpratik3-ai/MockMate`.
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** &gt; **Blueprint**.
4. Connect the `MockMate` GitHub repository.
5. Render will detect `render.yaml` and automatically configure:
   - **PostgreSQL Database**: `mockmate-db` (Free tier)
   - **FastAPI Web Service**: `mockmate-backend`
   - **Next.js Web Service**: `mockmate-frontend`
6. Add your `GEMINI_API_KEY` under the backend service environment variables.
7. Click **Apply**. Render will deploy the database and both services.

---

## 27. Production Configuration
- Backend binds to `0.0.0.0:$PORT` dynamically as required by Render.
- Frontend connects to `NEXT_PUBLIC_API_URL` pointing to the deployed backend URL.
- CORS is configured to accept requests from the deployed web frontend.
- Production PostgreSQL connection strings starting with `postgres://` are automatically normalized to `postgresql://` in `config.py`.

---

## 28. Security Considerations
- Passwords are encrypted using salted Bcrypt (rounds=12). Plaintext passwords are never stored.
- JWT tokens expire after 24 hours (`HS256` signature algorithm).
- All protected endpoints enforce user ownership (`interview.user_id == current_user.id`).
- Secrets and credentials are never checked into git. `.env` is strictly excluded via `.gitignore`.
- Inputs are strictly validated via Pydantic schemas.

---

## 29. Troubleshooting
- **CORS Error**: Ensure `NEXT_PUBLIC_API_URL` matches the exact URL of your backend service.
- **Port In Use**: Change `--port 8000` to `--port 8001` or kill conflicting processes.
- **Gemini Quota Exceeded**: MockMate automatically activates its verified domain question generator without crashing.
- **Database Connection Error**: Verify PostgreSQL service is healthy on Render or that local `DATABASE_URL` is accessible.

---

## 30. Known Limitations
- Voice/Audio recording mode is not part of this text/MCQ release.
- Free-tier Render web services spin down after 15 minutes of inactivity; initial cold start may take 30-50 seconds.

---

## 31. Future Enhancements
- Real-time speech-to-text audio interview simulation using WebRTC.
- Collaborative mock interviews with peer-to-peer room sharing.
- Resume upload & parsing to tailor questions specifically to past experience.
- Export scorecard as a verified PDF certificate.

---

## 32. License
This project is licensed under the MIT License.
