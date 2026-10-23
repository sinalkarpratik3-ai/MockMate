import pytest
import json
from unittest.mock import patch, AsyncMock
import httpx

from app.services.ai_service import ai_service


def test_five_consecutive_sessions_same_role(client, auth_headers):
    """
    Critical Regression Test 1:
    Verify that a user can start and complete at least FIVE consecutive practice tests
    for the same role (Java Developer) without hanging, stalling, or failing,
    and with zero within-session duplicate questions.
    """
    role = "Java Developer"
    difficulty = "Junior"
    mode = "mcq"
    num_questions = 5

    session_ids = []
    all_session_questions = []

    for session_idx in range(5):
        # 1. Create interview
        create_res = client.post(
            "/api/interviews/create",
            json={
                "job_role": role,
                "difficulty": difficulty,
                "mode": mode,
                "num_questions": num_questions
            },
            headers=auth_headers
        )
        assert create_res.status_code == 201, f"Session {session_idx+1} creation failed: {create_res.text}"
        itv_data = create_res.json()
        itv_id = itv_data["id"]
        assert itv_id is not None
        session_ids.append(itv_id)

        # 2. Retrieve interview details
        detail_res = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
        assert detail_res.status_code == 200
        questions = detail_res.json()["questions"]
        assert len(questions) == num_questions, f"Session {session_idx+1} expected {num_questions} questions, got {len(questions)}"

        # Verify Round 1 is Easy
        assert questions[0]["difficulty"] == "Easy", f"Session {session_idx+1} Round 1 difficulty must be Easy"

        # Verify that within THIS session, all question texts are distinct
        session_texts = [q["question_text"] for q in questions]
        assert len(set(session_texts)) == num_questions, f"Session {session_idx+1} contains duplicate questions within session: {session_texts}"

        # Verify all MCQs have valid 4 options
        for q in questions:
            opts = q.get("options")
            assert opts is not None and len(opts) == 4, f"Question {q['id']} in session {session_idx+1} must have 4 MCQ options"

        all_session_questions.append(session_texts)

        # 3. Submit answers in batch
        batch_answers = [
            {"question_id": q["id"], "selected_option": "A"}
            for q in questions
        ]
        submit_res = client.post(
            f"/api/interviews/{itv_id}/submit-batch",
            json={"answers": batch_answers},
            headers=auth_headers
        )
        assert submit_res.status_code == 200, f"Session {session_idx+1} submit-batch failed: {submit_res.text}"

        # 4. Complete interview
        complete_res = client.post(f"/api/interviews/{itv_id}/complete", headers=auth_headers)
        assert complete_res.status_code == 200
        completed = complete_res.json()
        assert completed["status"] == "completed"
        assert completed["total_score"] is not None
        assert completed["percentage"] >= 0.0

    # Verify that all 5 sessions received unique independent interview records
    assert len(set(session_ids)) == 5


def test_multi_role_repeated_sessions(client, auth_headers):
    """
    Critical Regression Test 2:
    Repeat practice tests across multiple diverse roles, difficulties, modes, and question counts:
    - Frontend Developer (Junior, MCQ, 5 questions)
    - Data Analyst (Mid-Level, MCQ, 5 questions)
    - DevOps Engineer (Junior, Text, 5 questions)
    - Database Administrator (Senior, MCQ, 5 questions)
    - Computer Networks (Junior, MCQ, 3 questions)
    - Machine Learning Engineer (Mid-Level, Text, 3 questions)
    - Custom Domain: Cloud Architect (Junior, MCQ, 5 questions)
    """
    test_cases = [
        {"role": "Frontend Developer", "difficulty": "Junior", "mode": "mcq", "count": 5},
        {"role": "Data Analyst", "difficulty": "Mid-Level", "mode": "mcq", "count": 5},
        {"role": "DevOps Engineer", "difficulty": "Junior", "mode": "text", "count": 5},
        {"role": "Database Administrator", "difficulty": "Senior", "mode": "mcq", "count": 5},
        {"role": "Computer Networks", "difficulty": "Junior", "mode": "mcq", "count": 3},
        {"role": "Machine Learning Engineer", "difficulty": "Mid-Level", "mode": "text", "count": 3},
        {"role": "Cloud Architect", "difficulty": "Junior", "mode": "mcq", "count": 5},
    ]

    for tc in test_cases:
        res = client.post(
            "/api/interviews/create",
            json={
                "job_role": tc["role"],
                "difficulty": tc["difficulty"],
                "mode": tc["mode"],
                "num_questions": tc["count"]
            },
            headers=auth_headers
        )
        assert res.status_code == 201, f"Failed to create interview for {tc['role']}: {res.text}"
        itv_id = res.json()["id"]

        detail_res = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
        assert detail_res.status_code == 200
        questions = detail_res.json()["questions"]
        assert len(questions) == tc["count"], f"Expected {tc['count']} questions for {tc['role']}, got {len(questions)}"

        # Verify Round 1 is Easy
        assert questions[0]["difficulty"] == "Easy"

        # Verify uniqueness within session
        q_texts = [q["question_text"] for q in questions]
        assert len(set(q_texts)) == tc["count"]

        # Verify options presence for MCQ or absence for Text
        for q in questions:
            if tc["mode"] == "mcq":
                assert q["options"] is not None and len(q["options"]) == 4
            else:
                assert q["options"] is None


def test_history_and_analytics_preserved(client, auth_headers):
    """
    Critical Regression Test 3:
    Verify that repeated practice sessions properly persist to history and analytics dashboards.
    """
    # Create and complete a test
    res = client.post(
        "/api/interviews/create",
        json={
            "job_role": "Python Developer",
            "difficulty": "Junior",
            "mode": "mcq",
            "num_questions": 3
        },
        headers=auth_headers
    )
    assert res.status_code == 201
    itv_id = res.json()["id"]

    detail_res = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
    questions = detail_res.json()["questions"]

    # Submit batch
    batch_answers = [{"question_id": q["id"], "selected_option": "A"} for q in questions]
    client.post(f"/api/interviews/{itv_id}/submit-batch", json={"answers": batch_answers}, headers=auth_headers)
    client.post(f"/api/interviews/{itv_id}/complete", headers=auth_headers)

    # Check interview list (history)
    hist_res = client.get("/api/interviews", headers=auth_headers)
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert any(item["id"] == itv_id for item in hist)

    # Check analytics dashboard
    analytics_res = client.get("/api/dashboard", headers=auth_headers)
    assert analytics_res.status_code == 200
    analytics_data = analytics_res.json()
    assert analytics_data["total_interviews"] >= 1


@pytest.mark.asyncio
async def test_ai_provider_rate_limit_resilience():
    """
    Critical Regression Test 4:
    Simulate external AI provider returning HTTP 429 Too Many Requests (Rate Limit/Quota Failure).
    Verify that MockMate breaks immediately and seamlessly falls back to verified domain questions
    without burning time or raising an exception.
    """
    mock_resp = AsyncMock(spec=httpx.Response)
    mock_resp.status_code = 429
    mock_resp.text = '{"error": {"code": 429, "message": "Resource exhausted / Quota exceeded"}}'

    with patch.object(httpx.AsyncClient, "post", return_value=mock_resp):
        questions = await ai_service.generate_questions(
            role="Java Developer",
            difficulty="Junior",
            mode="mcq",
            count=5
        )
        assert len(questions) == 5
        assert questions[0]["difficulty"] == "Easy"
        for q in questions:
            assert q["role"] == "Java Developer"
            assert "options" in q


@pytest.mark.asyncio
async def test_ai_provider_timeout_resilience():
    """
    Critical Regression Test 5:
    Simulate external AI provider timing out (httpx.TimeoutException).
    Verify that MockMate immediately catches the timeout and falls back to domain generator.
    """
    with patch.object(httpx.AsyncClient, "post", side_effect=httpx.TimeoutException("Read timed out after 4s")):
        questions = await ai_service.generate_questions(
            role="DevOps Engineer",
            difficulty="Junior",
            mode="mcq",
            count=5
        )
        assert len(questions) == 5
        assert questions[0]["difficulty"] == "Easy"
        assert len(set(q["question_text"] for q in questions)) == 5


@pytest.mark.asyncio
async def test_ai_provider_duplicate_and_malformed_response():
    """
    Critical Regression Test 6:
    Simulate external AI provider returning duplicate questions and invalid JSON.
    Verify that deduplication rejects invalid entries and supplements with verified questions.
    """
    # 1. Invalid JSON
    with patch.object(ai_service, "_call_gemini", return_value="NOT VALID JSON"):
        questions = await ai_service.generate_questions(
            role="Frontend Developer",
            difficulty="Junior",
            mode="mcq",
            count=5
        )
        assert len(questions) == 5
        assert len(set(q["question_text"] for q in questions)) == 5

    # 2. Duplicate questions in AI output
    dup_ai_json = json.dumps({
        "questions": [
            {
                "round_number": 1,
                "difficulty": "Easy",
                "topic": "HTML5",
                "question_text": "What does HTML stand for?",
                "options": [{"key": "A", "text": "HyperText Markup Language"}, {"key": "B", "text": "HighText"}, {"key": "C", "text": "HomeText"}, {"key": "D", "text": "None"}],
                "correct_option": "A"
            },
            {
                "round_number": 2,
                "difficulty": "Easy to Medium",
                "topic": "HTML5",
                "question_text": "What does HTML stand for?",  # Exact duplicate
                "options": [{"key": "A", "text": "HyperText Markup Language"}, {"key": "B", "text": "HighText"}, {"key": "C", "text": "HomeText"}, {"key": "D", "text": "None"}],
                "correct_option": "A"
            }
        ]
    })
    with patch.object(ai_service, "_call_gemini", return_value=dup_ai_json):
        questions = await ai_service.generate_questions(
            role="Frontend Developer",
            difficulty="Junior",
            mode="mcq",
            count=5
        )
        # Should have rejected the duplicate and supplemented up to 5 valid questions
        assert len(questions) == 5
        assert len(set(q["question_text"] for q in questions)) == 5
