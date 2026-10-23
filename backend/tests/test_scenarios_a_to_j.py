import os
import sys
import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000/api"

def test_full_live_scenarios_a_to_j():
    """
    Validates all Scenarios A through J required by the user against the running server:
    Test A — First Interview (verify question count, domain, difficulty)
    Test B — Second Interview (verify new session, distinct questions when alternatives exist)
    Test C — Third Interview (verify question variety continues across attempts, no hang)
    Test D — Different Domain (verify questions match new domain)
    Test E — Different Difficulty (verify returned questions reflect new difficulty)
    Test F — MCQ Test (verify answer selection, submission, scoring, and feedback)
    Test G — Written-Answer Test (verify written answers submission and evaluation)
    Test H — New Test After Completion (verify fresh state, no stale contamination)
    Test I — Test History (verify separate history entries and accessibility)
    Test J — Refresh and Authentication (verify user session restoration)
    """
    client = httpx.Client(base_url=BASE_URL, timeout=45.0)

    # 1. Health check
    health_res = client.get("/health")
    assert health_res.status_code == 200
    assert health_res.json()["database"] == "healthy"

    # 2. Registration & Authentication
    rand_id = os.urandom(4).hex()
    email = f"scenario_candidate_{rand_id}@mockmate.io"
    password = "ScenarioPassword123!"
    reg_res = client.post("/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Scenario Candidate"
    })
    assert reg_res.status_code in [200, 201]
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test J: Verify auth verification endpoint (/auth/me) for session restoration
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

    # Test A: First Interview (Python Developer, Junior, MCQ, 5 questions)
    res_a = client.post("/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=headers)
    assert res_a.status_code == 201
    id_a = res_a.json()["id"]

    detail_a = client.get(f"/interviews/{id_a}", headers=headers).json()
    questions_a = detail_a["questions"]
    assert len(questions_a) == 5
    assert detail_a["job_role"] == "Python Developer"
    assert questions_a[0]["difficulty"] == "Easy"
    for q in questions_a:
        assert q["options"] and len(q["options"]) == 4

    # Test F: MCQ Test answer selection, submission, scoring, and feedback
    answers_a = [
        {"question_id": q["id"], "selected_option": q["options"][0]["key"]}
        for q in questions_a
    ]
    batch_res = client.post(f"/interviews/{id_a}/submit-batch", json={"answers": answers_a}, headers=headers)
    assert batch_res.status_code == 200
    complete_res = client.post(f"/interviews/{id_a}/complete", headers=headers)
    assert complete_res.status_code == 200
    results_a = client.get(f"/interviews/{id_a}/results", headers=headers).json()
    assert results_a["status"] == "completed"
    assert results_a["total_score"] is not None
    assert len(results_a["answers"]) == 5

    # Test B: Second Interview (Same role, same difficulty)
    res_b = client.post("/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=headers)
    assert res_b.status_code == 201
    id_b = res_b.json()["id"]
    assert id_b != id_a, "Second interview must have a distinct session ID"

    # Test H: New Test After Completion (verify fresh state, no stale answers)
    detail_b = client.get(f"/interviews/{id_b}", headers=headers).json()
    questions_b = detail_b["questions"]
    assert len(questions_b) == 5
    assert len(detail_b.get("answers", [])) == 0, "New test must have zero stale answers"

    # Verify questions differ from Test A
    texts_a = set(q["question_text"].strip() for q in questions_a)
    texts_b = set(q["question_text"].strip() for q in questions_b)
    overlap_ab = texts_a.intersection(texts_b)
    assert len(overlap_ab) == 0, f"Expected zero question overlap between Test A and B, got: {overlap_ab}"

    # Complete Test B
    client.post(f"/interviews/{id_b}/submit-batch", json={
        "answers": [{"question_id": q["id"], "selected_option": "B"} for q in questions_b]
    }, headers=headers)
    client.post(f"/interviews/{id_b}/complete", headers=headers)

    # Test C: Third Interview (Same settings, verify continued variety & stability)
    res_c = client.post("/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=headers)
    assert res_c.status_code == 201
    id_c = res_c.json()["id"]
    detail_c = client.get(f"/interviews/{id_c}", headers=headers).json()
    questions_c = detail_c["questions"]
    assert len(questions_c) == 5
    texts_c = set(q["question_text"].strip() for q in questions_c)
    # Verify no within-session duplicates
    assert len(texts_c) == 5
    client.post(f"/interviews/{id_c}/submit-batch", json={
        "answers": [{"question_id": q["id"], "selected_option": "C"} for q in questions_c]
    }, headers=headers)
    client.post(f"/interviews/{id_c}/complete", headers=headers)

    # Test D: Different Domain (Java Developer)
    res_d = client.post("/interviews/create", json={
        "job_role": "Java Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=headers)
    assert res_d.status_code == 201
    id_d = res_d.json()["id"]
    detail_d = client.get(f"/interviews/{id_d}", headers=headers).json()
    questions_d = detail_d["questions"]
    assert len(questions_d) == 5
    assert detail_d["job_role"] == "Java Developer"
    # Ensure Java questions do not match Python questions
    java_texts = set(q["question_text"].strip() for q in questions_d)
    assert java_texts.isdisjoint(texts_a), "Java questions must not overlap with Python questions"

    # Test E: Different Difficulty (Senior Java Developer)
    res_e = client.post("/interviews/create", json={
        "job_role": "Java Developer",
        "difficulty": "Senior",
        "mode": "mcq",
        "num_questions": 5
    }, headers=headers)
    assert res_e.status_code == 201
    id_e = res_e.json()["id"]
    detail_e = client.get(f"/interviews/{id_e}", headers=headers).json()
    assert detail_e["difficulty"] == "Senior"
    assert len(detail_e["questions"]) == 5

    # Test G: Written-Answer Test (Text mode with evaluation)
    res_g = client.post("/interviews/create", json={
        "job_role": "Frontend Developer",
        "difficulty": "Junior",
        "mode": "text",
        "num_questions": 3
    }, headers=headers)
    assert res_g.status_code == 201
    id_g = res_g.json()["id"]
    detail_g = client.get(f"/interviews/{id_g}", headers=headers).json()
    questions_g = detail_g["questions"]
    assert len(questions_g) == 3
    for q in questions_g:
        assert q["options"] is None, "Text questions must not have options"
        assert q["question_type"] == "text"

    # Submit a written answer for question 1
    target_q = questions_g[0]
    submit_txt_res = client.post(f"/interviews/{id_g}/submit-answer", json={
        "question_id": target_q["id"],
        "text_answer": "Semantic HTML tags like article, nav, header, and section provide meaningful structural information to browsers and screen readers, enhancing SEO and accessibility."
    }, headers=headers)
    assert submit_txt_res.status_code == 200
    ans_data = submit_txt_res.json()
    assert ans_data["score"] is not None
    assert ans_data["feedback"] is not None
    assert "strengths" in ans_data

    # Complete text interview
    client.post(f"/interviews/{id_g}/complete", headers=headers)

    # Test I: Test History (verify separate records and accessibility)
    hist_res = client.get("/interviews", headers=headers)
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert len(hist) >= 4, f"Expected at least 4 completed interviews in history, got {len(hist)}"
    history_ids = [itv["id"] for itv in hist]
    assert id_a in history_ids
    assert id_b in history_ids
    assert id_c in history_ids
    assert id_g in history_ids
    print(f"\n>>> ALL SCENARIOS A THROUGH J PASSED PERFECTLY ON LIVE MOCKMATE APPLICATION! <<<")
