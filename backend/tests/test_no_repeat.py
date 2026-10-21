import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.models.user import User

client = TestClient(app)

def test_consecutive_interviews_have_no_repeated_questions():
    print("\n" + "=" * 65)
    print("TEST: NO REPEATED QUESTIONS ACROSS CONSECUTIVE SESSIONS")
    print("=" * 65)
    
    # 1. Register a dedicated test user
    email = f"norepeat_user_{os.urandom(4).hex()}@mockmate.io"
    password = "SecurePassword123!"
    
    reg_res = client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Dr. Diverse Questions"
    })
    assert reg_res.status_code in [200, 201], f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Session 1 (Frontend Developer, Mid-Level, 3 MCQs)
    print("\n[Session 1] Creating first interview...")
    res1 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Frontend Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 3
    })
    assert res1.status_code == 201, f"Failed session 1: {res1.text}"
    int1_id = res1.json()["id"]
    detail1 = client.get(f"/api/interviews/{int1_id}", headers=headers).json()
    q1_texts = [q["question_text"].strip() for q in detail1["questions"]]
    print(f"Session 1 Questions ({len(q1_texts)}):")
    for i, t in enumerate(q1_texts, 1):
        print(f"  [{i}] {t[:85]}...")

    # 3. Create Session 2 (Same role & difficulty)
    print("\n[Session 2] Creating second interview for same role & difficulty...")
    res2 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Frontend Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 3
    })
    assert res2.status_code == 201, f"Failed session 2: {res2.text}"
    int2_id = res2.json()["id"]
    detail2 = client.get(f"/api/interviews/{int2_id}", headers=headers).json()
    q2_texts = [q["question_text"].strip() for q in detail2["questions"]]
    print(f"Session 2 Questions ({len(q2_texts)}):")
    for i, t in enumerate(q2_texts, 1):
        print(f"  [{i}] {t[:85]}...")

    # Check overlap between Session 1 & Session 2
    overlap_1_2 = set(q1_texts).intersection(set(q2_texts))
    print(f"\nOverlap between Session 1 and Session 2: {len(overlap_1_2)}")
    assert len(overlap_1_2) == 0, f"Found repeated questions between 1 and 2: {overlap_1_2}"

    # 4. Create Session 3 (Same role & difficulty)
    print("\n[Session 3] Creating third interview for same role & difficulty...")
    res3 = client.post("/api/interviews/create", headers=headers, json={
        "job_role": "Frontend Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 3
    })
    assert res3.status_code == 201, f"Failed session 3: {res3.text}"
    int3_id = res3.json()["id"]
    detail3 = client.get(f"/api/interviews/{int3_id}", headers=headers).json()
    q3_texts = [q["question_text"].strip() for q in detail3["questions"]]
    print(f"Session 3 Questions ({len(q3_texts)}):")
    for i, t in enumerate(q3_texts, 1):
        print(f"  [{i}] {t[:85]}...")

    # Check all overlaps
    all_seen = q1_texts + q2_texts + q3_texts
    unique_seen = set(all_seen)
    print(f"\nTotal questions generated across 3 sessions: {len(all_seen)}")
    print(f"Unique distinct questions: {len(unique_seen)}")
    assert len(all_seen) == len(unique_seen), "Every single question must be unique across all sessions!"
    print("\n" + "=" * 65)
    print("SUCCESS: ALL QUESTIONS ACROSS ALL 3 CONSECUTIVE SESSIONS ARE 100% UNIQUE!")
    print("=" * 65)

if __name__ == "__main__":
    test_consecutive_interviews_have_no_repeated_questions()
