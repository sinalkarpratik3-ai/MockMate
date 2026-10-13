def test_interview_configuration_validation(client, auth_headers):
    # Invalid role
    res = client.post("/api/interviews/create", json={
        "job_role": "Invalid Unknown Role",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    assert res.status_code == 400

    # Invalid difficulty
    res = client.post("/api/interviews/create", json={
        "job_role": "Frontend Developer",
        "difficulty": "Master",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    assert res.status_code == 400

    # Invalid mode
    res = client.post("/api/interviews/create", json={
        "job_role": "Frontend Developer",
        "difficulty": "Junior",
        "mode": "voice",
        "num_questions": 3
    }, headers=auth_headers)
    assert res.status_code == 400

def test_mcq_interview_workflow(client, auth_headers):
    # 1. Create MCQ interview
    res = client.post("/api/interviews/create", json={
        "job_role": "Frontend Developer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 3
    }, headers=auth_headers)
    assert res.status_code == 201
    interview = res.json()
    itv_id = interview["id"]
    assert interview["status"] == "in_progress"

    # 2. Get interview details
    res_detail = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
    assert res_detail.status_code == 200
    questions = res_detail.json()["questions"]
    assert len(questions) == 3
    
    # Verify no leaked correct answers during active test
    for q in questions:
        assert "correct_option" not in q or q.get("correct_option") is None
        assert len(q["options"]) == 4

    # 3. Submit an answer for first question
    q1 = questions[0]
    res_ans = client.post(f"/api/interviews/{itv_id}/submit-answer", json={
        "question_id": q1["id"],
        "selected_option": "B"
    }, headers=auth_headers)
    assert res_ans.status_code == 200
    ans_data = res_ans.json()
    assert ans_data["selected_option"] == "B"
    assert "score" in ans_data

    # 4. Complete interview
    res_comp = client.post(f"/api/interviews/{itv_id}/complete", headers=auth_headers)
    assert res_comp.status_code == 200
    comp_data = res_comp.json()
    assert comp_data["status"] == "completed"
    assert "percentage" in comp_data
    assert comp_data["completed_at"] is not None

def test_text_interview_workflow(client, auth_headers):
    # 1. Create text interview
    res = client.post("/api/interviews/create", json={
        "job_role": "Backend Developer",
        "difficulty": "Senior",
        "mode": "text",
        "num_questions": 2
    }, headers=auth_headers)
    assert res.status_code == 201
    itv_id = res.json()["id"]

    res_detail = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
    questions = res_detail.json()["questions"]
    assert len(questions) == 2

    # 2. Submit text response
    q1 = questions[0]
    ans_text = (
        "In a microservices architecture, asynchronous communication via message brokers "
        "like Kafka or RabbitMQ decouples services and prevents cascading failures. "
        "Eventual consistency can be managed using the Saga pattern with compensating transactions."
    )
    res_ans = client.post(f"/api/interviews/{itv_id}/submit-answer", json={
        "question_id": q1["id"],
        "text_answer": ans_text
    }, headers=auth_headers)
    assert res_ans.status_code == 200
    ans_eval = res_ans.json()
    assert ans_eval["score"] >= 0 and ans_eval["score"] <= 10
    assert "feedback" in ans_eval

    # 3. Complete interview
    res_comp = client.post(f"/api/interviews/{itv_id}/complete", headers=auth_headers)
    assert res_comp.status_code == 200
    assert res_comp.json()["status"] == "completed"

def test_user_data_isolation(client, auth_headers, auth_headers_user2):
    # User 1 creates interview
    res1 = client.post("/api/interviews/create", json={
        "job_role": "Python Developer",
        "difficulty": "Junior",
        "mode": "mcq",
        "num_questions": 2
    }, headers=auth_headers)
    itv_id = res1.json()["id"]

    # User 2 tries to access User 1's interview -> 403 Forbidden
    res2 = client.get(f"/api/interviews/{itv_id}", headers=auth_headers_user2)
    assert res2.status_code == 403

def test_bookmarks_lifecycle(client, auth_headers):
    # Create interview to obtain a question
    res = client.post("/api/interviews/create", json={
        "job_role": "DevOps Engineer",
        "difficulty": "Mid-Level",
        "mode": "mcq",
        "num_questions": 1
    }, headers=auth_headers)
    itv_id = res.json()["id"]
    res_detail = client.get(f"/api/interviews/{itv_id}", headers=auth_headers)
    q_id = res_detail.json()["questions"][0]["id"]

    # Bookmark question
    res_bm = client.post(f"/api/bookmarks/{q_id}", headers=auth_headers)
    assert res_bm.status_code in [200, 201]

    # Verify bookmark listed
    res_list = client.get("/api/bookmarks", headers=auth_headers)
    assert res_list.status_code == 200
    bms = res_list.json()
    assert any(b["question_id"] == q_id for b in bms)

    # Remove bookmark
    res_del = client.delete(f"/api/bookmarks/{q_id}", headers=auth_headers)
    assert res_del.status_code == 200

def test_daily_question_and_dashboard(client, auth_headers):
    # 1. Daily Question
    res_daily = client.get("/api/daily", headers=auth_headers)
    assert res_daily.status_code == 200
    daily_data = res_daily.json()
    assert "question_text" in daily_data
    assert "date" in daily_data

    # Submit daily answer
    res_attempt = client.post("/api/daily/attempt", json={
        "submitted_answer": "A"
    }, headers=auth_headers)
    assert res_attempt.status_code == 201

    # Duplicate daily attempt rejected
    res_dupe = client.post("/api/daily/attempt", json={
        "submitted_answer": "B"
    }, headers=auth_headers)
    assert res_dupe.status_code == 400

    # 2. Dashboard summary
    res_dash = client.get("/api/dashboard", headers=auth_headers)
    assert res_dash.status_code == 200
    dash_data = res_dash.json()
    assert "total_interviews" in dash_data
    assert "total_questions_attempted" in dash_data
    assert "mcq_accuracy_pct" in dash_data
    assert "avg_text_score" in dash_data
    assert "weak_topics" in dash_data
    assert dash_data["has_attempted_daily"] is True
