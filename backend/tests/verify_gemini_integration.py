import os
import sys
import json
import asyncio
import httpx
from unittest.mock import AsyncMock, patch

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.services.ai_service import ai_service
from app.services.evaluation_service import evaluation_service
from app.models.question import Question

results = {}

def run_diagnostics():
    print("=" * 60)
    print("MOCKMATE GEMINI API INTEGRATION & FALLBACK VERIFICATION")
    print("=" * 60)

    # 1. Environment Configuration Check
    key_val = settings.GEMINI_API_KEY
    has_key = bool(key_val and len(key_val.strip()) > 10)
    results["env_config"] = "PASS" if has_key else "FAIL"
    print(f"\n[1] Environment Configuration: {results['env_config']}")
    print(f"    - GEMINI_API_KEY configured: {'YES (masked: ' + key_val[:4] + '...' + key_val[-4:] + ')' if has_key else 'NO'}")
    print(f"    - Configured Model: {settings.GEMINI_MODEL}")

    # 2. Network Reachability & Authentication
    print("\n[2] Network Connectivity & Authentication Test:")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key_val}"
    try:
        r = httpx.get(list_url, timeout=10.0)
        results["network"] = "PASS"
        print(f"    - Network Connectivity: PASS (HTTP status {r.status_code})")
        if r.status_code == 200:
            results["auth"] = "PASS"
            available_models = [m["name"].replace("models/", "") for m in r.json().get("models", [])]
            print(f"    - API Authentication: PASS (Key validated by Google, returned {len(available_models)} models)")
            
            # 3. Model Availability
            model_found = settings.GEMINI_MODEL in available_models
            results["model_avail"] = "PASS" if model_found else "UNKNOWN"
            print(f"    - Configured Model ({settings.GEMINI_MODEL}) in list: {'PASS' if model_found else 'NOT FOUND'}")
        elif r.status_code == 400:
            results["auth"] = "FAIL (Invalid API key)"
            print(f"    - API Authentication: FAIL - Google returned 400 API_KEY_INVALID")
            available_models = []
        else:
            results["auth"] = f"FAIL (HTTP {r.status_code})"
            print(f"    - API Authentication: FAIL (HTTP {r.status_code})")
            available_models = []
    except Exception as exc:
        results["network"] = f"FAIL ({exc})"
        results["auth"] = "FAIL"
        available_models = []
        print(f"    - Network Connectivity: FAIL - {exc}")

    # 4. Content Generation Permissions & Quota Diagnostics
    print("\n[3] Content Generation Permission & Live API Diagnostics:")
    test_models = [settings.GEMINI_MODEL, "gemini-pro-latest", "gemini-1.5-flash"]
    quota_diagnosis = {}
    
    for m in test_models:
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key_val}"
        try:
            res = httpx.post(
                gen_url, 
                json={"contents": [{"parts": [{"text": "Hello, respond with: OK"}]}]}, 
                timeout=10.0
            )
            if res.status_code == 200:
                quota_diagnosis[m] = "PASS"
                print(f"    - Model '{m}': PASS (HTTP 200 OK - Live response received)")
            else:
                err_data = res.json().get("error", {})
                err_status = err_data.get("status", "UNKNOWN")
                err_code = err_data.get("code", res.status_code)
                err_msg = err_data.get("message", res.text)[:140]
                quota_diagnosis[m] = f"HTTP {err_code} {err_status}"
                print(f"    - Model '{m}': HTTP {err_code} {err_status}")
                print(f"      Sanitized Error: {err_msg}...")
        except Exception as ex:
            quota_diagnosis[m] = f"ERROR: {ex}"
            print(f"    - Model '{m}': Request error: {ex}")

    # 5. Live Question Generation vs Fallback
    print("\n[4] Question Generation Test (Role: Frontend Developer, Level: Mid-Level, Format: MCQ, Count: 3):")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # First check raw live call
        raw_live = loop.run_until_complete(ai_service._call_gemini("Generate 3 questions"))
        if raw_live is not None:
            results["live_q_gen"] = "PASS"
            print("    - Live API Call: PASS (Live text received from Gemini)")
        else:
            results["live_q_gen"] = "BLOCKED"
            print("    - Live API Call: BLOCKED (Live API returned 429/403/Quota exhausted)")

        # Next run the full service method
        questions = loop.run_until_complete(
            ai_service.generate_questions("Frontend Developer", "Mid-Level", "mcq", 3)
        )
        print(f"    - Returned Questions Count: {len(questions)}")
        assert len(questions) == 3, "Expected 3 questions"
        for idx, q in enumerate(questions):
            opts = json.loads(q["options"])
            assert len(opts) == 4, f"Question {idx+1} must have 4 options"
            assert q["correct_option"] in ["A", "B", "C", "D"], f"Question {idx+1} has invalid correct_option"
            assert len(q["question_text"]) > 10, f"Question {idx+1} question_text is empty"
            assert len(q["explanation"]) > 5, f"Question {idx+1} explanation is empty"
            print(f"      Q{idx+1}: {q['question_text'][:60]}... [Correct: {q['correct_option']}] (Topic: {q['topic']})")
        results["q_gen_schema"] = "PASS"
        print("    - Question Schema Validation: PASS (All questions have text, topic, 4 options, valid answer & explanation)")
    except Exception as exc:
        results["q_gen_schema"] = f"FAIL ({exc})"
        print(f"    - Question Generation: FAIL - {exc}")

    # 6. Live Written-Answer Evaluation vs Fallback
    print("\n[5] Written-Answer Evaluation Test:")
    sample_q = "Explain the difference between useEffect and useLayoutEffect in React."
    sample_ans = "useEffect runs asynchronously after paint, while useLayoutEffect runs synchronously immediately after DOM mutations before paint, making useLayoutEffect ideal for DOM measurements."
    
    try:
        eval_raw = loop.run_until_complete(
            ai_service._call_gemini(f"Evaluate this answer: {sample_ans}")
        )
        if eval_raw is not None:
            results["live_eval"] = "PASS"
            print("    - Live Evaluation Call: PASS")
        else:
            results["live_eval"] = "BLOCKED"
            print("    - Live Evaluation Call: BLOCKED (Live API blocked by quota/permissions)")

        eval_res = loop.run_until_complete(
            ai_service.evaluate_text_answer("Frontend Developer", "Mid-Level", sample_q, sample_ans, "React Hooks")
        )
        print(f"    - Evaluation Score: {eval_res['score']} / 10")
        print(f"    - Feedback: {eval_res['feedback'][:80]}...")
        print(f"    - Strengths returned: {len(eval_res['strengths'])}")
        print(f"    - Missing concepts returned: {len(eval_res['missing_concepts'])}")
        print(f"    - Sample answer provided: {bool(eval_res['model_answer'])}")
        assert 0.0 <= eval_res["score"] <= 10.0, "Score out of range"
        assert len(eval_res["strengths"]) > 0, "No strengths"
        results["eval_schema"] = "PASS"
        print("    - Evaluation Schema Validation: PASS")
    except Exception as exc:
        results["eval_schema"] = f"FAIL ({exc})"
        print(f"    - Evaluation Schema: FAIL - {exc}")

    # 7. Fallback Simulation Scenarios (429, 401/403, 500/503, Timeout, Malformed JSON)
    print("\n[6] Fallback Resilience Simulation (Testing all failure modes):")
    simulated_scenarios = [
        ("HTTP 429 Quota Exceeded", httpx.Response(429, json={"error": {"code": 429, "message": "Quota exceeded"}})),
        ("HTTP 401 Authentication Failure", httpx.Response(401, json={"error": {"code": 401, "message": "Invalid key"}})),
        ("HTTP 403 Permission Denied", httpx.Response(403, json={"error": {"code": 403, "message": "Access denied"}})),
        ("HTTP 500 Internal Server Error", httpx.Response(500, text="Internal Server Error")),
        ("HTTP 503 Service Unavailable", httpx.Response(503, text="Service Unavailable")),
        ("Network Timeout", httpx.ConnectTimeout("Connection timed out")),
        ("Malformed JSON", httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": "NOT_JSON_<<<"}]}}]}))
    ]

    all_fallback_passed = True
    for scenario_name, mock_response in simulated_scenarios:
        async def mock_post(*args, **kwargs):
            if isinstance(mock_response, Exception):
                raise mock_response
            return mock_response

        with patch("httpx.AsyncClient.post", side_effect=mock_post):
            try:
                # Test question generation fallback
                fb_qs = loop.run_until_complete(
                    ai_service.generate_questions("Backend Developer", "Senior", "mcq", 3)
                )
                assert len(fb_qs) == 3, f"Expected 3 fallback questions for {scenario_name}"
                
                # Test text evaluation fallback
                fb_eval = loop.run_until_complete(
                    ai_service.evaluate_text_answer("Backend Developer", "Senior", "Explain database indexing", "B-trees create balanced trees", "Databases")
                )
                assert 0.0 <= fb_eval["score"] <= 10.0, "Fallback score out of range"
                assert len(fb_eval["strengths"]) > 0, "No fallback strengths"
                print(f"    - {scenario_name}: PASS (Handled gracefully, returned {len(fb_qs)} questions & valid evaluation)")
            except Exception as ex:
                all_fallback_passed = False
                print(f"    - {scenario_name}: FAIL ({ex})")

    results["fallback"] = "PASS" if all_fallback_passed else "FAIL"

    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_diagnostics()
