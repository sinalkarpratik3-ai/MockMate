# MockMate: Interview Preparation Platform

![MockMate Banner](https://img.shields.io/badge/MockMate-Interview%20Preparation%20Platform-24483F?style=for-the-badge&logoColor=white)
![Build Status](https://img.shields.io/badge/Tests-12%2F12%20Passing-367451?style=for-the-badge)
![Render Ready](https://img.shields.io/badge/Render-Deployment%20Ready-24483F?style=for-the-badge&logo=render)

---

## 1. Project Title
**MockMate — Interview Preparation Platform**

---

## 2. Project Overview
MockMate is a professional, human-centred interview preparation platform designed to help software engineers prepare for technical interviews with clarity and confidence. The platform provides structured practice sessions across multiple software engineering roles and experience levels, pairing multiple-choice conceptual quizzes with written technical answer assessments, detailed constructive feedback, sample answers, and persistent progress tracking.

Rather than treating interview preparation as a technology demonstration, MockMate focuses on the candidate's learning experience: helping users identify knowledge gaps, practice structured explanations, review sample solutions, and build lasting interview confidence.

---

## 3. Problem Statement
Technical interview preparation is frequently fragmented, stressful, and unstructured:
- Static question banks quickly grow repetitive, lack difficulty calibration, and fail to test deep practical reasoning.
- Practicing standalone algorithm puzzles does not prepare candidates for architectural discussions, system design trade-offs, or conceptual deep-dives.
- Peer practice interviews are hard to schedule consistently, yield variable feedback quality, and lack objective historical performance records.
- Candidates rarely have clear diagnostic insight into which exact technical concepts pull down their interview performance over time.

---

## 4. Primary Objectives
1. Provide a focused, distraction-free technical interview practice platform with dynamic session creation.
2. Deliver complementary assessment formats: rapid-fire multiple-choice quizzes and in-depth written answer evaluations.
3. Offer constructive feedback highlighting strengths, key concepts to review, and clear engineering sample answers.
4. Persist all practice attempts, answers, and scores in a production-ready database (PostgreSQL with SQLite fallback).
5. Track progress over time to identify weak topics (<60% accuracy) and offer direct targeted practice.
6. Provide a Daily Challenge to foster a consistent, daily practice habit.
7. Maintain strict security, user data isolation, and 100% compatibility with standard GitHub and Render deployment workflows.

---

## 5. Visual Identity and Design System
MockMate uses an earthy, grounded, and professional visual identity designed for readability, focus, and comfort during long study sessions. The interface deliberately avoids generic purple-to-blue SaaS gradients, glowing artificial elements, or distracting novelty graphics.

### Palette Tokens
- **Forest Green (`#24483F`)**: Primary actions, active navigation tabs, major headings, and confirmed selections.
- **Deep Charcoal (`#252923`)**: Primary body text, labels, and high-contrast content.
- **Warm Cream (`#F7F3EA`)**: Dominant application canvas background.
- **Soft Sage (`#DCE6D8`)**: Secondary surfaces, subtle highlights, active badges, and focus rings.
- **Terracotta (`#C66A4A`)**: Intentional secondary accent for daily challenge callouts and alert badges.
- **Muted Olive (`#879477`)**: Metadata, subheadings, and chart visualisations.
- **Warm Sand (`#E8DDCA`)**: Card borders, dividers, and neutral surface framing.
- **Muted Grey (`#777B74`)**: Secondary descriptions and supporting copy.
- **Success Green (`#367451`)**: Correct answers and completed session indicators.
- **Error Red (`#B8473F`)**: Form validation errors and incorrect answer indicators.
- **Pure White (`#FFFFFF`)**: Reserved selectively for high-readability card surfaces and form inputs.

---

## 6. Shneiderman’s Eight Golden Rules Implementation
The entire interface has been engineered adhering strictly to Ben Shneiderman’s Eight Golden Rules of Interface Design:

1. **Consistency**: Unified color tokens, typography scales, card layouts, and interaction patterns across all 13 modules.
2. **Universal Usability**: Fully responsive across mobile, tablet, and desktop viewports with accessible contrast ratios.
3. **Informative Feedback**: Clear progress indicators during session creation, answer submission, and bookmarking.
4. **Dialogues with Closure**: Well-defined sequence flows: Configure Session &rarr; Complete Questions &rarr; Submit &rarr; Review Scorecard.
5. **Error Prevention**: Form validation prevents blank submissions; destructive actions require confirmation dialogs.
6. **Easy Reversal**: Users can freely navigate between questions before submission and toggle saved question bookmarks.
7. **User Control**: Explicit user actions trigger submissions; tests are never automatically submitted without confirmation.
8. **Reduce Memory Load**: Target role, difficulty level, current question number, and progress meters remain persistently visible.

---

## 7. Supported Engineering Tracks & Difficulty Tiers

### Tracks
1. **Frontend Developer**: Modern React architecture, TypeScript, DOM internals, CSS architecture, Core Web Vitals, state management.
2. **Backend Developer**: REST APIs, database indexing, caching strategies, microservices architecture, API authentication.
3. **Python Developer**: Asyncio, GIL, memory management, generators, decorators, clean object-oriented design.
4. **Java Developer**: JVM internals, Spring Boot ecosystem, thread safety, garbage collection tuning, Hibernate.
5. **DevOps Engineer**: Containerisation, Kubernetes, CI/CD pipelines, Terraform, Linux networking, high availability.
6. **Data Analyst**: Complex SQL queries, window functions, pandas, data validation, metrics definition, statistical insights.

### Difficulty Levels
- **Junior**: Fundamental syntax, standard libraries, data structures, and foundational concepts.
- **Mid-Level**: Design patterns, API optimization, error handling, and database query tuning.
- **Senior**: Distributed systems, architectural trade-offs, scalability, and system reliability.

---

## 8. Practice Formats

### Format A: Multiple Choice Practice
- **Format**: Curated 4-option questions (A, B, C, D).
- **Integrity**: Correct answers and explanations are hidden during active testing to ensure honest self-assessment.
- **Evaluation**: Instant deterministic scoring on submission (`is_correct = (selected == correct_option)`).
- **Navigation**: Previous/Next navigation, question jump palette, progress meter, and confirmation modal.
- **Review**: Detailed breakdown displaying candidate choice, correct answer, status badges, and thorough technical explanations.

### Format B: Written Answers Practice
- **Format**: Comfortable multiline response editor for articulating system design trade-offs, algorithms, and technical concepts.
- **Evaluation**: Reviewed against key evaluation dimensions:
  1. Conceptual correctness
  2. Technical depth and mechanics
  3. Clarity and structure
  4. Practical trade-offs and real-world examples
  5. Essential terminology coverage
- **Output**: Constructive 0-to-10 score, "What You Did Well", "Key Concepts to Review", practical suggestions for improvement, and a complete engineering sample answer.

---

## 9. Core Functional Modules
1. **User Authentication & Session Security**: Registration, secure login, password hashing, and JWT token isolation.
2. **Practice Session Configuration**: Guided setup for role, difficulty tier, format, and question count.
3. **Multiple-Choice Workspace**: Distraction-free question workspace with question palette navigation.
4. **Written-Answer Workspace**: Multiline answer editor with instant answer review and sample answer comparison.
5. **Question Generation Service**: Structured service layer that provides relevant questions for the selected role and tier.
6. **Answer Evaluation Engine**: Deterministic MCQ grading and structured rubric-based written evaluation.
7. **Scorecard & Detailed Review**: Final scores, points earned, question breakdowns, and explanations.
8. **Progress Tracking**: Aggregated database statistics tracking sessions, accuracy, and scores over time.
9. **Topics to Revisit**: Diagnostic detection of concepts with <60% accuracy with direct one-click practice links.
10. **Practice History**: Searchable, chronological archive of past sessions with quick resumption and review actions.
11. **Saved Questions (Revision Notebook)**: Personal notebook to bookmark questions, sample answers, and explanations.
12. **Question of the Day**: Rotating daily challenge that builds habit with duplicate attempt prevention.
13. **Account & Profile Settings**: Clean account information, session security overview, and logout control.

---

## 10. Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router, Turbopack, React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4 with custom earthy theme tokens
- **Icons**: Lucide React
- **Architecture**: Modular components, React Context state management, custom typed fetch client

### Backend
- **Framework**: Python FastAPI
- **Data Validation**: Pydantic v2 & Pydantic-Settings
- **ORM & Database**: SQLAlchemy 2.0 (PostgreSQL in production, SQLite fallback for local testing)
- **Security**: Native Bcrypt password hashing, Python-Jose (JWT HS256 tokens)
- **Content Service Layer**: Asynchronous content generation service with structured schema parsing and resilience engine
- **Testing**: Pytest & Pytest-Asyncio

---

## 11. System Architecture
```text
┌─────────────────────────────────────────────────────────────────┐
│                       Next.js Frontend                          │
│     (Landing, Dashboard, Workspace, Results, Bookmarks, Daily)  │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTPS / JSON (REST API)
┌────────────────────────────────▼────────────────────────────────┐
│                     FastAPI Backend Service                     │
│  ┌──────────────────┬───────────────────┬──────────────────┐    │
│  │ Auth & Security  │ Practice Service  │ Analytics Engine │    │
│  └─────────┬────────┴─────────┬─────────┴─────────┬────────┘    │
└────────────┼──────────────────┼───────────────────┼─────────────┘
             │                  │                   │
             ▼                  ▼                   ▼
    ┌─────────────────┐ ┌────────────────┐  ┌──────────────────┐
    │   PostgreSQL    │ │ Content Engine │  │ Local Resilience │
    │    Database     │ │ Service Layer  │  │  Domain Engine   │
    └─────────────────┘ └────────────────┘  └──────────────────┘
```

---

## 12. Project Directory Structure
```text
MockMate/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Registration, login, current user
│   │   │   ├── interviews.py    # Session creation, answer submission, results
│   │   │   ├── bookmarks.py     # Bookmark management
│   │   │   ├── daily.py         # Question of the Day & attempt tracking
│   │   │   ├── dashboard.py     # Aggregated summary & KPIs
│   │   │   └── health.py        # System health & database heartbeat
│   │   ├── core/
│   │   │   ├── config.py        # Application configuration & settings
│   │   │   ├── database.py      # SQLAlchemy engine & sessionmaker
│   │   │   └── security.py      # Bcrypt password hashing & JWT handling
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # Users table
│   │   │   ├── interview.py     # Interviews table
│   │   │   ├── question.py      # Questions table
│   │   │   ├── answer.py        # Evaluated answers table
│   │   │   ├── bookmark.py      # Bookmarks table
│   │   │   └── daily.py         # DailyQuestions & DailyAttempts tables
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Authentication schemas
│   │   │   ├── interview.py     # Interview schemas
│   │   │   ├── question.py      # Question schemas
│   │   │   ├── answer.py        # Answer schemas
│   │   │   ├── bookmark.py      # Bookmark schemas
│   │   │   ├── daily.py         # Daily question schemas
│   │   │   └── dashboard.py     # Dashboard metrics schemas
│   │   ├── services/
│   │   │   ├── auth_service.py       # Authentication business logic
│   │   │   ├── ai_service.py         # Content generation service & fallbacks
│   │   │   ├── interview_service.py  # Interview lifecycle management
│   │   │   ├── evaluation_service.py # MCQ & written answer grading
│   │   │   └── analytics_service.py  # Progress calculations & weak topics
│   │   └── main.py              # FastAPI application entrypoint
│   ├── tests/
│   │   ├── conftest.py          # Pytest fixtures & isolated test DB
│   │   ├── test_auth.py         # Authentication test cases
│   │   └── test_interviews.py   # Interview workflows & analytics tests
│   └── requirements.txt         # Backend Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout & AuthProvider
│   │   │   ├── globals.css      # Theme variables & custom scrollbars
│   │   │   ├── page.tsx         # Landing page
│   │   │   ├── login/page.tsx   # Login page
│   │   │   ├── register/page.tsx# Registration page
│   │   │   ├── dashboard/page.tsx   # Dashboard
│   │   │   ├── interviews/
│   │   │   │   ├── new/page.tsx     # Setup & configuration page
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx     # Distraction-free question workspace
│   │   │   │       └── results/page.tsx # Scorecard & review page
│   │   │   ├── history/page.tsx     # Practice history
│   │   │   ├── bookmarks/page.tsx   # Saved questions notebook
│   │   │   ├── daily/page.tsx       # Question of the day
│   │   │   ├── analytics/page.tsx   # Your progress
│   │   │   └── profile/page.tsx     # Profile & settings
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Header navigation
│   │   │   ├── Sidebar.tsx      # Sidebar navigation
│   │   │   └── AppLayout.tsx    # Auth guard & page shell
│   │   ├── context/
│   │   │   └── AuthContext.tsx  # Auth state & token storage
│   │   ├── lib/
│   │   │   └── api.ts           # Fetch client with auth headers
│   │   └── types/
│   │       └── index.ts         # TypeScript data types
│   ├── package.json
│   └── tsconfig.json
│
├── render.yaml                  # Render Blueprint deployment definition
├── .env.example                 # Environment variables reference
├── .gitignore
└── README.md
```

---

## 13. Prerequisites
- **Python**: 3.10, 3.11, 3.12, 3.13, or 3.14
- **Node.js**: v18+, v20+ (LTS recommended)
- **Package Managers**: `pip` and `npm`
- **PostgreSQL**: Optional for local development (defaults to SQLite if PostgreSQL is not active; PostgreSQL used in production).

---

## 14. Local Installation Instructions

Clone the repository:
```bash
git clone https://github.com/sinalkarpratik3-ai/MockMate.git
cd MockMate
```

### Frontend Setup
```bash
cd frontend
npm install
```

Configure `.env.local` inside `frontend/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend Setup
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

## 15. Technical Content Service Configuration
The backend includes a pluggable content generation layer for generating dynamic questions and reviewing written responses:
1. If using an external generation service, set `GEMINI_API_KEY` in `backend/.env`:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```
2. If no external key is configured, MockMate seamlessly activates its verified domain engineering bank to guarantee 100% operational uptime without interruption.

---

## 16. Environment Variables Reference
| Variable | Required | Description | Default |
|---|---|---|---|
| `DATABASE_URL` | No | PostgreSQL / SQLite connection string | `sqlite:///./mockmate.db` |
| `SECRET_KEY` | Yes (in prod) | Secret key for JWT encryption | `super-secret-jwt-key` |
| `GEMINI_API_KEY` | Optional | Content generation service key | `""` |
| `GEMINI_MODEL` | No | Model name | `gemini-1.5-flash` |
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL for frontend client | `http://localhost:8000/api` |

---

## 17. Running the Application Locally

### Start Backend
```bash
cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API runs at `http://127.0.0.1:8000` (Interactive API docs at `http://127.0.0.1:8000/api/docs`).

### Start Frontend
```bash
cd frontend
npm run dev
```
Web application runs at `http://localhost:3000`.

---

## 18. Running the Test Suite
MockMate includes 12 automated unit and integration tests covering authentication, session lifecycle, deterministic MCQ grading, written evaluation rubrics, question bookmarks, daily challenge locking, and user data isolation:

```bash
cd backend
.venv\Scripts\Activate.ps1
pytest tests -v
```

Expected output:
```text
======================= 12 passed in 10.32s ========================
```

---

## 19. Render Deployment Guide
The project includes a complete Render Blueprint (`render.yaml`):

1. Push your repository to GitHub: `https://github.com/sinalkarpratik3-ai/MockMate`.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New +** &rarr; **Blueprint**.
3. Select your `MockMate` repository.
4. Render automatically configures:
   - **PostgreSQL Database**: `mockmate-db`
   - **FastAPI Web Service**: `mockmate-backend`
   - **Next.js Web Service**: `mockmate-frontend`
5. Set `GEMINI_API_KEY` in the backend service environment settings if using an external generation service.
6. Click **Apply** to deploy the database and web services.

---

## 20. Security and Data Protection
- Passwords are encrypted using salted Bcrypt (rounds=12); plaintext passwords are never stored.
- JWT tokens expire after 24 hours (`HS256` signature algorithm).
- All protected endpoints enforce strict user ownership (`interview.user_id == current_user.id`).
- Secrets and credentials are strictly excluded via `.gitignore`.
- Inputs are validated via Pydantic schemas before reaching the database.

---

## 21. License
This project is licensed under the MIT License.
