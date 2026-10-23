import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def test_complete_practice_interview_flow_sequence():
    """
    Verifies the end-to-end multi-test flow:
    1. Create Junior Python Developer MCQ test (5 questions) -> verify 5 questions load.
    2. Submit answers & complete the first test.
    3. Create a second test with the same settings -> verify 5 questions load, new ID, fresh state, no stale answers.
    4. Create a Written Answers test (Junior Python Developer, text mode, 5 questions) -> verify 5 questions load.
    5. Create a different role & difficulty (Senior Java Developer) -> verify session starts successfully.
    """
    # Step 0: Register a clean test user
    email = f"practice_flow_{os.urandom(4).hex()}@mockmate.io"
    password = "SecurePassword123!"
    
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Practice Flow Candidate"
    })
    assert reg_res.status_code in [200, 201], f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 1: Create first test - Junior Python Developer, MCQ, 5 questions
    res1 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    })
    assert res1.status_code == 201, f"Test 1 creation failed: {res1.text}"
    int1_data = res1.json()
    int1_id = int1_data["id"]
    assert int1_data["status"] == "in_progress"
    assert int1_data["num_questions"] == 5

    # Verify all 5 questions load for Test 1
    detail1 = client.get(f"/api/interviews/{int1_id}", headers=headers).json()
    questions1 = detail1["questions"]
    assert len(questions1) == 5, f"Expected 5 questions in test 1, got {len(questions1)}"
    for q in questions1:
        assert q["question_text"] and len(q["question_text"]) > 10
        assert q["options"] and len(q["options"]) == 4

    # Step 2: Submit answers and complete Test 1
    batch_answers1 = [
        {"question_id": q["id"], "selected_option": "A"}
        for q in questions1
    ]
    sub1 = client.post(f"/api/interviews/{int1_id}/submit-batch", headers=headers, json={
        "answers": batch_answers1
    })
    assert sub1.status_code == 200, f"Submit batch failed: {sub1.text}"
    completed1 = sub1.json()
    assert completed1["status"] == "completed"
    assert completed1["completed_at"] is not None
    assert len(completed1["answers"]) == 5

    # Verify Results view
    res1_view = client.get(f"/api/interviews/{int1_id}/results", headers=headers)
    assert res1_view.status_code == 200
    assert res1_view.json()["status"] == "completed"

    # Step 3: Create second test with the EXACT SAME SETTINGS
    res2 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    })
    assert res2.status_code == 201, f"Test 2 creation failed: {res2.text}"
    int2_data = res2.json()
    int2_id = int2_data["id"]
    assert int2_id != int1_id, "Second test must have a distinct new session ID"
    assert int2_data["status"] == "in_progress"
    assert int2_data["num_questions"] == 5

    # Verify all 5 questions load for Test 2 and state is fresh
    detail2 = client.get(f"/api/interviews/{int2_id}", headers=headers).json()
    questions2 = detail2["questions"]
    assert len(questions2) == 5, f"Expected 5 questions in test 2, got {len(questions2)}"
    assert len(detail2.get("answers", [])) == 0, "Second test must have empty answers initially (no stale answers)"

    # Verify that Test 2 questions are distinct from Test 1 questions
    q1_texts = [q["question_text"].strip() for q in questions1]
    q2_texts = [q["question_text"].strip() for q in questions2]
    overlap = set(q1_texts).intersection(set(q2_texts))
    assert len(overlap) == 0, f"Second test must not duplicate test 1 questions: {overlap}"

    # Complete Test 2
    batch_answers2 = [
        {"question_id": q["id"], "selected_option": "B"}
        for q in questions2
    ]
    sub2 = client.post(f"/api/interviews/{int2_id}/submit-batch", headers=headers, json={
        "answers": batch_answers2
    })
    assert sub2.status_code == 200
    assert sub2.json()["status"] == "completed"

    # Step 4: Repeat using Written Answers (Junior Python Developer, text mode, 5 questions)
    res3 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "text",
        "num_questions": 5
    })
    assert res3.status_code == 201, f"Written Answers test creation failed: {res3.text}"
    int3_id = res3.json()["id"]
    detail3 = client.get(f"/api/interviews/{int3_id}", headers=headers).json()
    assert detail3["mode"] == "text"
    assert len(detail3["questions"]) == 5
    # Submit one answer and complete text interview
    first_q = detail3["questions"][0]
    txt_sub = client.post(f"/api/interviews/{int3_id}/submit-answer", headers=headers, json={
        "question_id": first_q["id"],
        "text_answer": "In Python, immutable objects cannot be altered in memory once created, while mutable objects can."
    })
    assert txt_sub.status_code == 200
    comp3 = client.post(f"/api/interviews/{int3_id}/complete", headers=headers)
    assert comp3.status_code == 200
    assert comp3.json()["status"] == "completed"

    # Step 5: Verify a different role and difficulty can start a session
    res4 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Java Developer",
        "difficulty": "Senior",
        "mode": "mcq",
        "num_questions": 5
    })
    assert res4.status_code == 201, f"Different role test creation failed: {res4.text}"
    int4_id = res4.json()["id"]
    detail4 = client.get(f"/api/interviews/{int4_id}", headers=headers).json()
    assert detail4["job_role"] == "Java Developer"
    assert detail4["difficulty"] == "Senior"
    assert len(detail4["questions"]) == 5
