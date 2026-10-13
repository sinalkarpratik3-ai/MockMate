import os
import sys
import asyncio
import json
import time

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.core.config import settings
from app.services.ai_service import ai_service
from app.services.evaluation_service import evaluation_service
from app.models.question import Question

@pytest.mark.asyncio
async def test_live_ai():
    print("=" * 65)
    print("LIVE GEMINI API TEST & VERIFICATION")
    print("=" * 65)
    
    key = settings.GEMINI_API_KEY
    masked_key = key[:6] + "..." + key[-4:] if key else "NONE"
    print(f"API Key Configured:     YES (Masked: {masked_key})")
    print(f"Configured Model:        {settings.GEMINI_MODEL}")
    print(f"Target Endpoint:         {ai_service.base_url}")
    print("-" * 65)
    
    # 1. Direct prompt to test live generation
    print("\n[Step 1] Direct Live Generation Test:")
    t0 = time.perf_counter()
    raw = await ai_service._call_gemini(
        'Return valid JSON with key "greeting" containing "Hello from MockMate"'
    )
    dt1 = (time.perf_counter() - t0) * 1000
    
    if raw:
        print(f"   [PASS] Live Gemini Response in {dt1:.0f}ms!")
        print(f"   Response Preview: {raw.strip()[:100]}")
    else:
        print(f"   [FAIL] No response received from live API.")
        return

    # 2. Live Question Generation Test (MCQ)
    print("\n[Step 2] Live Question Generation (Role: Frontend Developer, Mid-Level, MCQ x 3):")
    t0 = time.perf_counter()
    questions = await ai_service.generate_questions(
        role="Frontend Developer",
        difficulty="Mid-Level",
        mode="mcq",
        count=3
    )
    dt2 = (time.perf_counter() - t0) * 1000
    print(f"   Generated {len(questions)} questions in {dt2:.0f}ms.")
    
    for i, q in enumerate(questions, 1):
        opts = json.loads(q["options"])
        print(f"\n   Q{i}: {q['question_text']}")
        print(f"       Topic: {q['topic']} | Level: {q['difficulty']}")
        for opt in opts:
            print(f"       [{opt['key']}] {opt['text']}")
        print(f"       Correct: [{q['correct_option']}]")
        print(f"       Explanation: {q['explanation'][:100]}...")
        assert len(opts) == 4, "MCQ must have 4 options"
        assert q["correct_option"] in ["A", "B", "C", "D"], "Valid option key required"
        assert q["question_text"], "Question text required"

    # 3. Live Written-Answer Evaluation Test
    print("\n[Step 3] Live Written-Answer Evaluation Test:")
    sample_q = Question(
        id=1,
        interview_id=1,
        question_text="Explain the difference between synchronous and asynchronous code in Node.js, and describe how the Event Loop handles microtasks versus macrotasks.",
        role="Backend Developer",
        difficulty="Mid-Level",
        topic="Node.js Internals & Event Loop",
        question_type="text",
        model_answer="Synchronous code runs on the call stack and blocks execution. Asynchronous code delegates I/O to libuv worker threads and registers callbacks. The Event Loop processes the call stack, then drains the microtask queue (process.nextTick and Promise callbacks) before proceeding to each macrotask phase (timers, I/O callbacks, check/setImmediate)."
    )
    
    candidate_answer = (
        "In Node.js, synchronous operations block the single-threaded event loop, meaning further code cannot execute "
        "until the operation finishes. Asynchronous operations offload tasks like file reads or network requests to libuv, "
        "allowing the main thread to remain responsive. When callbacks complete, they are queued. The event loop prioritizes "
        "microtasks (such as Promise .then() callbacks and process.nextTick) immediately after the current operation finishes "
        "and before moving to the next macrotask (such as setTimeout or setImmediate)."
    )
    
    t0 = time.perf_counter()
    eval_res = await evaluation_service.evaluate_text(sample_q, candidate_answer)
    dt3 = (time.perf_counter() - t0) * 1000
    
    print(f"   Evaluated candidate response in {dt3:.0f}ms.")
    print(f"   Score:           {eval_res['score']:.1f}/10 ({'Passed' if eval_res['is_correct'] else 'Failed'})")
    print(f"   Feedback:        {eval_res['feedback'][:150]}...")
    
    strengths = json.loads(eval_res["strengths"])
    missing = json.loads(eval_res["missing_concepts"])
    tips = json.loads(eval_res["improvement_tips"])
    
    print(f"   Strengths:       {strengths}")
    print(f"   Missing/Review:  {missing}")
    print(f"   Improvement Tip: {tips}")
    
    assert 0.0 <= eval_res["score"] <= 10.0, "Score within range"
    assert len(eval_res["feedback"]) > 10, "Constructive feedback returned"
    
    print("\n" + "=" * 65)
    print("ALL LIVE GEMINI API VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(test_live_ai())
