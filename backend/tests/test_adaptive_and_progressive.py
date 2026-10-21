import os
import sys
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.ai_service import ai_service
from app.services.question_banks import (
    normalize_question_text,
    is_duplicate_or_near_duplicate,
    get_round_difficulty,
    adapt_difficulty,
    get_topics_for_role,
    DIFFICULTY_PROGRESSION,
)

# Test 1: Initial difficulty is always Easy
def test_initial_difficulty_is_easy(client, auth_headers):
    """Confirm the first question of every new interview is Easy."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=auth_headers)
    assert res.status_code == 201
    itv = res.json()
    assert itv["current_round"] == 1
    assert itv["current_difficulty"] == "Easy"

    detail = client.get(f"/api/interviews/{itv['id']}", headers=auth_headers).json()
    assert len(detail["questions"]) == 5
    first_q = detail["questions"][0]
    assert first_q["round_number"] == 1
    assert first_q["difficulty"].lower() == "easy"


# Test 2: Progressive difficulty advances across rounds
def test_progressive_difficulty_progression(client, auth_headers):
    """Verify that questions advance progressively from Easy -> Easy to Medium -> Medium -> Medium to Hard -> Hard."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Java Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 5
    }, headers=auth_headers)
    assert res.status_code == 201
    detail = client.get(f"/api/interviews/{res.json()['id']}", headers=auth_headers).json()
    questions = detail["questions"]
    assert len(questions) == 5

    difficulties = [q["difficulty"] for q in questions]
    # Check that initial is Easy and later questions progress to Harder tiers
    assert difficulties[0] == "Easy"
    assert difficulties[1] in ["Easy to Medium", "Medium"]
    assert difficulties[2] in ["Medium", "Easy to Medium", "Medium to Hard"]
    assert difficulties[-1] in ["Hard", "Medium to Hard"]

    # Verify unit progression mapping function directly
    prog = [get_round_difficulty(r, 5) for r in range(1, 6)]
    assert prog == ["Easy", "Easy to Medium", "Medium", "Medium to Hard", "Hard"]


# Test 3: Adaptive difficulty responds to user answers
def test_adaptive_difficulty_adjustment(client, auth_headers):
    """Simulate low score and verify system reinforces with suitable intermediate difficulty."""
    # Test adapt_difficulty unit logic directly
    assert adapt_difficulty("Hard", score_percentage=25.0) == "Medium"
    assert adapt_difficulty("Hard", score_percentage=45.0) == "Medium to Hard"
    assert adapt_difficulty("Medium to Hard", score_percentage=25.0) == "Easy to Medium"
    assert adapt_difficulty("Medium", score_percentage=90.0) == "Medium to Hard"
    assert adapt_difficulty("Easy", score_percentage=85.0) == "Easy to Medium"
    assert adapt_difficulty("Easy", score_percentage=20.0) == "Easy"

    # Integration: create text interview, submit low score answer
    res = client.post("/api/interviews/create", json={
        "job_role": "Backend Developer",
        "difficulty": "Senior",
        "mode": "text",
        "num_questions": 3
    }, headers=auth_headers)
    itv_id = res.json()["id"]
    detail = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()
    q1 = detail["questions"][0]

    # Submit an empty or poor answer
    sub_res = client.post(f"/api/interviews/{itv_id}/submit-answer", json={
        "question_id": q1["id"],
        "text_answer": "I do not know."
    }, headers=auth_headers)
    assert sub_res.status_code == 200

    # Verify interview did not crash or reset to Round 0
    updated_itv = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()
    assert updated_itv["current_round"] >= 1


# Test 4: Domain relevance
def test_domain_relevance():
    """Verify topics and questions match the selected domain."""
    python_topics = get_topics_for_role("Python Developer")
    assert any("asyncio" in t.lower() or "gil" in t.lower() or "generator" in t.lower() for t in python_topics)

    networks_topics = get_topics_for_role("Computer Networks")
    assert any("osi" in t.lower() or "tcp" in t.lower() or "dns" in t.lower() for t in networks_topics)

    dba_topics = get_topics_for_role("Database Administrator")
    assert any("acid" in t.lower() or "indexing" in t.lower() or "normalization" in t.lower() for t in dba_topics)

    ml_topics = get_topics_for_role("Machine Learning Engineer")
    assert any("overfitting" in t.lower() or "gradient" in t.lower() or "evaluation" in t.lower() for t in ml_topics)


# Test 5: Repetition prevention with exact and near-duplicates
def test_repetition_prevention():
    """Test text normalization and near-duplicate detection."""
    q_orig = "What is the Global Interpreter Lock (GIL) in Python?"
    q_near = "Explain the Python Global Interpreter Lock (GIL) and its effects on multithreading."
    q_exact = "what is the global interpreter lock gil in python???"
    q_different = "How does the Python garbage collector handle cyclic references?"

    assert is_duplicate_or_near_duplicate(q_exact, [q_orig]) is True
    assert is_duplicate_or_near_duplicate(q_near, [q_orig]) is True
    assert is_duplicate_or_near_duplicate(q_different, [q_orig]) is False


# Test 6: More than two questions without repeating
def test_generate_ten_distinct_questions(client, auth_headers):
    """Generate 10 questions and verify no two questions are identical or repeating."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 10
    }, headers=auth_headers)
    assert res.status_code == 201
    detail = client.get(f"/api/interviews/{res.json()['id']}", headers=auth_headers).json()
    questions = detail["questions"]
    assert len(questions) == 10

    texts = [q["question_text"].strip() for q in questions]
    normalized = [normalize_question_text(t) for t in texts]
    assert len(set(normalized)) == 10, "All 10 questions must be completely distinct!"


# Test 7: API failure graceful fallback
@pytest.mark.asyncio
async def test_api_failure_fallback_behavior():
    """Simulate API failure (e.g. quota exhausted / 503 unavailable) and confirm valid domain fallback."""
    with patch.object(ai_service, "_call_gemini", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = None  # Simulates API unavailable
        fallback_qs = await ai_service.generate_questions(
            role="Web Developer",
            difficulty="Junior",
            mode="mcq",
            count=5
        )
        assert len(fallback_qs) == 5
        # Verify fallback questions are valid, easy on round 1, and Web Developer focused
        assert fallback_qs[0]["round_number"] == 1
        assert fallback_qs[0]["difficulty"] == "Easy"
        for q in fallback_qs:
            assert q["question_text"]
            assert len(q["options"]) > 0


# Test 8: Session persistence
def test_session_persistence(client, auth_headers):
    """Verify that round, difficulty, and question history remain consistent across fetches."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Machine Learning Engineer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    itv_id = res.json()["id"]

    # First fetch
    fetch1 = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()
    # Second fetch (simulating page reload)
    fetch2 = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()

    assert fetch1["id"] == fetch2["id"]
    assert fetch1["current_round"] == fetch2["current_round"]
    assert fetch1["current_difficulty"] == fetch2["current_difficulty"]
    assert [q["id"] for q in fetch1["questions"]] == [q["id"] for q in fetch2["questions"]]


# Test 9: Concurrent / duplicate submission handling
def test_duplicate_submission_handling(client, auth_headers):
    """Verify duplicate answer submission does not create duplicate database records."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Computer Networks",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    itv_id = res.json()["id"]
    detail = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()
    q1_id = detail["questions"][0]["id"]

    # Submit answer
    sub1 = client.post(f"/api/interviews/{itv_id}/submit-answer", json={
        "question_id": q1_id,
        "selected_option": "A"
    }, headers=auth_headers)
    assert sub1.status_code == 200

    # Resubmit answer for same question (update)
    sub2 = client.post(f"/api/interviews/{itv_id}/submit-answer", json={
        "question_id": q1_id,
        "selected_option": "B"
    }, headers=auth_headers)
    assert sub2.status_code == 200

    # Check answers count is 1, not 2
    detail_after = client.get(f"/api/interviews/{itv_id}", headers=auth_headers).json()
    q1_answers = [a for a in detail_after["answers"] if a["question_id"] == q1_id]
    assert len(q1_answers) == 1
    assert q1_answers[0]["selected_option"] == "B"


# Test 10: Unsupported role rejection
def test_unsupported_role_rejected(client, auth_headers):
    """Verify unsupported role is clearly rejected with 400 Bad Request."""
    res = client.post("/api/interviews/create", json={
        "job_role": "Invalid Unknown Role",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    assert res.status_code == 400
    assert "Unsupported domain" in res.json()["detail"]
