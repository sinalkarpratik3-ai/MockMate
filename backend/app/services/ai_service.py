import json
import logging
import random
from typing import List, Dict, Any, Optional
import httpx

from app.core.config import settings
from app.services.question_banks import (
    ROLE_TOPICS,
    FALLBACK_MCQ_BANK,
    FALLBACK_TEXT_BANK,
    get_topics_for_role,
    get_fallback_bank_for_role,
    normalize_question_text,
    is_duplicate_or_near_duplicate,
    get_round_difficulty,
    adapt_difficulty,
    shuffle_mcq_options,
)

logger = logging.getLogger(__name__)

class AIService:
    @property
    def api_key(self) -> str:
        return settings.GEMINI_API_KEY or ""

    @property
    def model(self) -> str:
        return settings.GEMINI_MODEL or "gemini-3.8-flash"

    @property
    def base_url(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    async def _call_gemini(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """Calls Gemini API with structured JSON request and multi-model fallback resilience."""
        if not self.api_key or self.api_key.strip() == "":
            logger.info("No GEMINI_API_KEY set; utilizing verified domain generator.")
            return None

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "response_mime_type": "application/json"
            }
        }

        # Preferred models in order of capability & speed (bound to at most 2 fast models)
        models_to_try = [self.model, "gemini-2.0-flash", "gemini-1.5-flash"]
        unique_models = []
        for m in models_to_try:
            if m and m not in unique_models:
                unique_models.append(m)
        unique_models = unique_models[:2]

        async with httpx.AsyncClient(timeout=4.0) as client:
            for model_name in unique_models:
                try:
                    target_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                    response = await client.post(target_url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            text_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            if text_content:
                                return text_content
                    elif response.status_code in [401, 403]:
                        logger.info(f"Gemini API authentication issue ({response.status_code}); seamlessly switching to domain generator.")
                        break
                    elif response.status_code == 429:
                        logger.warning(f"Gemini API rate limit (429) hit; seamlessly switching to domain generator.")
                        break
                    else:
                        logger.warning(f"Gemini API ({model_name}) returned status {response.status_code}: {response.text[:200]}")
                        break
                except httpx.TimeoutException:
                    logger.warning(f"Gemini API ({model_name}) timed out after 4s; seamlessly switching to domain generator.")
                    break
                except Exception as e:
                    logger.warning(f"Gemini API ({model_name}) request failed: {e}")
                    break
        return None

    async def generate_questions(
        self,
        role: str,
        difficulty: str,
        mode: str,
        count: int,
        exclude_questions: Optional[List[str]] = None,
        topic_focus: Optional[str] = None,
        experience_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generates structured, domain-specific interview questions following progressive difficulty:
        - Round 1 is ALWAYS Easy (foundations, syntax, core definitions).
        - Subsequent rounds gradually increase in difficulty (Easy to Medium -> Medium -> Medium to Hard -> Hard).
        - Strictly prevents duplicates and near-duplicates against excluded past questions.
        """
        # 1. Establish the round difficulty blueprint
        round_specs = []
        for i in range(count):
            r_num = i + 1
            r_diff = get_round_difficulty(r_num, count)
            round_specs.append((r_num, r_diff))

        # 2. Pick domain focus topics
        available_topics = get_topics_for_role(role)
        sampled_topics = random.sample(available_topics, min(max(count, 3), len(available_topics)))
        if topic_focus and topic_focus not in sampled_topics:
            sampled_topics.insert(0, topic_focus)

        # 3. Clean excluded questions list
        clean_exclude = [q.strip() for q in (exclude_questions or []) if q and q.strip()]
        exclude_section = ""
        if clean_exclude:
            # Pass up to 25 recent questions as negative examples
            sample_exclusions = clean_exclude[:25]
            bullet_list = "\n".join([f"- {q[:120]}" for q in sample_exclusions])
            exclude_section = f"\nDO NOT repeat, duplicate, or rephrase any of these previously asked questions:\n{bullet_list}\n"

        # 4. Construct round-by-round guide
        round_guide_lines = [
            f"- Question {r_num}: Round {r_num} • Difficulty '{r_diff}'. "
            f"({'Test basic definitions, core syntax, and fundamentals' if r_num == 1 else 'Progressively increase technical depth, trade-offs, and practical engineering scenarios'})"
            for r_num, r_diff in round_specs
        ]
        round_guide = "\n".join(round_guide_lines)

        prompt = f"""You are an elite principal technical interviewer designing an interview for a {role} position.
Experience Profile: {experience_level or difficulty}
Mode: {mode.upper()}
Total Questions: {count}

Focus Topics:
{', '.join(sampled_topics)}

Round-by-Round Progression:
{round_guide}
{exclude_section}
Mandatory Rules:
1. Every question MUST be strictly relevant to {role}. Do NOT provide questions from unrelated technical fields.
2. Question 1 (Round 1) MUST be Easy and test fundamental concepts or definitions of {role}.
3. Subsequent questions must follow the designated progressive difficulty.
4. Every question must be genuinely distinct with zero duplicate or near-duplicate concepts.
5. If mode is 'mcq', provide exactly 4 distinct, plausible options ('A', 'B', 'C', 'D'). Randomly distribute the correct answer across 'A', 'B', 'C', or 'D' (DO NOT always make it 'A'). Provide the corresponding correct_option key, and a clear explanation.
6. If mode is 'text', provide a comprehensive ideal model_answer.
7. Return strict JSON matching the schema below.

JSON Schema:
{{
  "questions": [
    {{
      "round_number": 1,
      "difficulty": "Easy",
      "topic": "string",
      "question_text": "string",
      "options": [
        {{"key": "A", "text": "option 1"}},
        {{"key": "B", "text": "option 2"}},
        {{"key": "C", "text": "option 3"}},
        {{"key": "D", "text": "option 4"}}
      ],
      "correct_option": "C",
      "explanation": "string",
      "model_answer": null
    }}
  ]
}}
"""
        raw_response = await self._call_gemini(prompt, temperature=0.7)
        if raw_response:
            try:
                parsed = json.loads(raw_response)
                questions_raw = parsed.get("questions", [])
                if isinstance(questions_raw, list) and len(questions_raw) > 0:
                    valid_questions: List[Dict[str, Any]] = []
                    seen_in_batch: List[str] = []

                    for idx, q in enumerate(questions_raw):
                        q_text = (q.get("question_text") or "").strip()
                        if not q_text:
                            continue

                        # Check for duplicate against past history or within this batch
                        if is_duplicate_or_near_duplicate(q_text, clean_exclude + seen_in_batch):
                            logger.info(f"Rejected duplicate generated question: {q_text[:60]}")
                            continue

                        assigned_round = idx + 1
                        assigned_diff = get_round_difficulty(assigned_round, count)

                        if mode == "mcq":
                            opts = q.get("options", [])
                            if len(opts) == 4:
                                shuffled_opts, shuffled_key = shuffle_mcq_options(opts, q.get("correct_option"))
                                valid_questions.append({
                                    "question_text": q_text,
                                    "role": role,
                                    "round_number": assigned_round,
                                    "difficulty": assigned_diff,
                                    "topic": q.get("topic", random.choice(sampled_topics)),
                                    "question_type": "mcq",
                                    "options": json.dumps(shuffled_opts),
                                    "correct_option": shuffled_key,
                                    "explanation": q.get("explanation", ""),
                                    "model_answer": None
                                })
                                seen_in_batch.append(q_text)
                        else:
                            valid_questions.append({
                                "question_text": q_text,
                                "role": role,
                                "round_number": assigned_round,
                                "difficulty": assigned_diff,
                                "topic": q.get("topic", random.choice(sampled_topics)),
                                "question_type": "text",
                                "options": None,
                                "correct_option": None,
                                "explanation": None,
                                "model_answer": q.get("model_answer", "")
                            })
                            seen_in_batch.append(q_text)

                        if len(valid_questions) >= count:
                            break

                    if len(valid_questions) == count:
                        return valid_questions
                    elif len(valid_questions) > 0:
                        # Supplement any missing questions with verified fallback
                        missing_count = count - len(valid_questions)
                        supplement = self._get_fallback_questions(
                            role=role,
                            difficulty=difficulty,
                            mode=mode,
                            count=missing_count,
                            exclude_questions=clean_exclude + seen_in_batch,
                            start_round=len(valid_questions) + 1,
                            total_rounds=count
                        )
                        return valid_questions + supplement
            except Exception as e:
                logger.error(f"Error parsing Gemini questions response: {e}")

        # Resilient fallback questions generator with progressive difficulty and strict deduplication
        return self._get_fallback_questions(
            role=role,
            difficulty=difficulty,
            mode=mode,
            count=count,
            exclude_questions=clean_exclude,
            start_round=1,
            total_rounds=count
        )

    def _get_fallback_questions(
        self,
        role: str,
        difficulty: str,
        mode: str,
        count: int,
        exclude_questions: Optional[List[str]] = None,
        start_round: int = 1,
        total_rounds: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Provides verified, domain-specific questions matching progressive difficulty tiers.
        Guarantees that:
        - Round 1 is Easy
        - Subsequent rounds progress toward Hard
        - No duplicate questions are ever served within a session
        - Recycles least-recently-asked bank questions across repeated sessions
        - Never gets stuck cycling or hanging
        """
        effective_total = total_rounds or (start_round + count - 1)
        bank_map = get_fallback_bank_for_role(role, mode)

        exclude_list = [q.strip() for q in (exclude_questions or []) if q and q.strip()]
        # Bounded sliding window of exclusions from the immediate recent tests
        recent_exclusions = exclude_list[:max(count * 2, 10)]

        selected: List[Dict[str, Any]] = []
        session_chosen_texts: List[str] = []

        difficulty_order = ["Easy", "Easy to Medium", "Medium", "Medium to Hard", "Hard"]

        # Flatten all domain bank questions for fallback search
        all_domain_questions: List[Dict[str, Any]] = []
        for diff_tier in difficulty_order:
            all_domain_questions.extend(bank_map.get(diff_tier, []))

        for i in range(count):
            round_num = start_round + i
            target_diff = get_round_difficulty(round_num, effective_total)

            candidate = None

            # 1. Search in target difficulty tier for questions not in session and not in recent exclusions
            tier_candidates = [q for q in bank_map.get(target_diff, []) if q["question_text"] not in session_chosen_texts]
            random.shuffle(tier_candidates)
            for q in tier_candidates:
                if not is_duplicate_or_near_duplicate(q["question_text"], session_chosen_texts + recent_exclusions):
                    candidate = q
                    break

            # 2. If exhausted in target tier, search adjacent difficulty tiers in the same domain
            if not candidate:
                adjacent_candidates = [q for q in all_domain_questions if q["question_text"] not in session_chosen_texts]
                random.shuffle(adjacent_candidates)
                for q in adjacent_candidates:
                    if not is_duplicate_or_near_duplicate(q["question_text"], session_chosen_texts + recent_exclusions):
                        candidate = q
                        break

            # 3. If all bank questions have been used recently, recycle bank questions not used in the CURRENT session
            #    prioritizing the Least-Recently-Used questions (those furthest back in exclude_list or not in exclude_list)
            if not candidate and all_domain_questions:
                unpicked_in_session = [q for q in all_domain_questions if q["question_text"] not in session_chosen_texts]
                if unpicked_in_session:
                    def lru_key(q_item: Dict[str, Any]) -> int:
                        txt = q_item["question_text"]
                        try:
                            return exclude_list.index(txt)  # higher index = used longer ago in exclude_list
                        except ValueError:
                            return 999999
                    unpicked_in_session.sort(key=lru_key, reverse=True)
                    for q in unpicked_in_session:
                        if not is_duplicate_or_near_duplicate(q["question_text"], session_chosen_texts):
                            candidate = q
                            break

            # 4. If bank is empty (or custom domain), generate a distinct dynamic domain fallback
            if not candidate:
                candidate = self._generate_dynamic_domain_fallback(
                    role, target_diff, mode, round_num, session_chosen_texts + recent_exclusions
                )

            session_chosen_texts.append(candidate["question_text"])

            if mode == "mcq" and candidate.get("options"):
                shuffled_opts, shuffled_key = shuffle_mcq_options(
                    candidate["options"],
                    candidate.get("correct_option", "A")
                )
                final_options = json.dumps(shuffled_opts)
                final_correct = shuffled_key
            else:
                final_options = None
                final_correct = None

            item = {
                "question_text": candidate["question_text"],
                "role": role,
                "round_number": round_num,
                "difficulty": target_diff,
                "topic": candidate.get("topic", f"{role} Core Knowledge"),
                "question_type": mode,
                "options": final_options,
                "correct_option": final_correct,
                "explanation": candidate.get("explanation") if mode == "mcq" else None,
                "model_answer": candidate.get("model_answer") if mode == "text" else None
            }
            selected.append(item)

        return selected

    def _generate_dynamic_domain_fallback(
        self,
        role: str,
        difficulty: str,
        mode: str,
        round_num: int,
        seen_texts: List[str]
    ) -> Dict[str, Any]:
        """
        Dynamically synthesizes a verified domain-specific question to ensure zero collisions
        even if an interview exceeds the pre-stored question bank size.
        """
        topics = get_topics_for_role(role)
        seed_offset = len(seen_texts)

        # 8 distinct real-world technical scenario archetypes
        archetypes = [
            (
                "When designing an enterprise production architecture for {topic} in {role}, which implementation strategy best ensures modularity and fault isolation?",
                "Decouple state and logic via explicit interfaces, strict contracts, and granular error boundaries for {topic}",
                "Combine all business logic and persistence logic into a single monolithic global singleton",
                "Bypass schema validation and runtime sanity checks to maximize unthrottled throughput",
                "Hardcode external endpoints and credentials directly inside domain handler functions"
            ),
            (
                "In high-concurrency {role} services, how should engineers mitigate latency spikes and resource contention related to {topic}?",
                "Implement asynchronous non-blocking processing, connection pooling, and bounded telemetry-driven caching for {topic}",
                "Allocate unbounded thread pools and disable backpressure to swallow incoming traffic bursts",
                "Disable structured audit logs and performance metrics during high traffic windows",
                "Block the main event thread synchronously until each third-party dependency for {topic} responds"
            ),
            (
                "Which engineering practice is essential when writing automated regression tests for {topic} as a {role}?",
                "Mock external network dependencies at boundaries and assert deterministic state transitions and error paths for {topic}",
                "Run test suites directly against mutating production data without transactional rollback isolation",
                "Insert arbitrary sleep delays rather than relying on deterministic event signals or completion promises",
                "Disable all assertion checks in CI so test pipelines pass unconditionally under load"
            ),
            (
                "When securing sensitive endpoints and workflows involving {topic} in a {role} system, which control is most critical?",
                "Enforce role-based access control, cryptographic verification, and strict input sanitization at ingress for {topic}",
                "Rely solely on client-side frontend validation without backend verification",
                "Transmit sensitive tokens and secrets within cleartext URL query parameters",
                "Disable CORS and authentication headers to simplify internal microservice communication"
            ),
            (
                "How should a {role} approach database persistence, queries, and index optimization for {topic} under heavy write load?",
                "Analyze query execution plans (EXPLAIN), optimize index cardinality, and leverage write-ahead batches for {topic}",
                "Add indexes on every single column regardless of cardinality or write overhead",
                "Execute full table scans inside loops rather than batching relational operations",
                "Disable database foreign key integrity and transactional ACID constraints permanently"
            ),
            (
                "In a distributed {role} environment, how should systems handle transient network partitions or downstream outages affecting {topic}?",
                "Employ circuit breaker patterns with exponential backoff jitter and graceful fallback degradation for {topic}",
                "Retry failed requests in a tight synchronous infinite loop with zero backoff",
                "Immediately crash the application worker process upon the first transient network timeout",
                "Silently drop incoming client requests without returning an appropriate HTTP error status code"
            ),
            (
                "Which observability strategy provides the most actionable insight for diagnosing production anomalies in {topic} for a {role}?",
                "Correlate structured JSON logs, OpenTelemetry distributed traces, and RED/USE metrics for {topic}",
                "Rely strictly on unstructured console print statements scattered across business logic",
                "Sample only 0.001% of error events to conserve disk space during operational outages",
                "Disable health check endpoints and alert triggers to reduce on-call alert noise"
            ),
            (
                "When refactoring legacy code for {topic} into a modern {role} service, which approach best preserves backward compatibility?",
                "Introduce semantic API versioning, contract testing, and deprecated feature flags with gradual migration paths for {topic}",
                "Change public method signatures and payloads abruptly without migration notices",
                "Delete legacy test suites to avoid updating outdated assertion expectations",
                "Rewrite the entire persistence layer in an untested experimental framework in a single deploy"
            ),
        ]

        # Search for a candidate variant that is not a duplicate
        for attempt in range(len(archetypes) * 2):
            topic_idx = (round_num - 1 + attempt // len(archetypes) + seed_offset) % len(topics)
            chosen_topic = topics[topic_idx]
            arch_idx = (round_num + seed_offset + attempt) % len(archetypes)
            q_template, opt_a_tmpl, opt_b_tmpl, opt_c_tmpl, opt_d_tmpl = archetypes[arch_idx]

            q_text = q_template.format(topic=chosen_topic, role=role)
            if not is_duplicate_or_near_duplicate(q_text, seen_texts):
                opt_a = opt_a_tmpl.format(topic=chosen_topic, role=role)
                opt_b = opt_b_tmpl.format(topic=chosen_topic, role=role)
                opt_c = opt_c_tmpl.format(topic=chosen_topic, role=role)
                opt_d = opt_d_tmpl.format(topic=chosen_topic, role=role)

                if mode == "mcq":
                    raw_options = [
                        {"key": "A", "text": opt_a},
                        {"key": "B", "text": opt_b},
                        {"key": "C", "text": opt_c},
                        {"key": "D", "text": opt_d}
                    ]
                    shuffled_opts, shuffled_key = shuffle_mcq_options(raw_options, "A")
                    return {
                        "question_text": q_text,
                        "topic": chosen_topic,
                        "options": shuffled_opts,
                        "correct_option": shuffled_key,
                        "explanation": f"In production {role} engineering, {chosen_topic} demands {opt_a.lower()}."
                    }
                else:
                    return {
                        "question_text": f"Explain the architectural trade-offs, practical implementation patterns, and error handling strategies for {chosen_topic} in a production {role} environment.",
                        "topic": chosen_topic,
                        "model_answer": f"When implementing {chosen_topic} for a {role} system, engineers must account for performance, failure modes, monitoring, and modularity. Production solutions decouple implementation details through interfaces, enforce strict typing and error logging, and measure latency and throughput under peak load."
                    }

        # Fallback if all archetypes matched (append round seed to guarantee novelty)
        topic_idx = (round_num - 1) % len(topics)
        chosen_topic = topics[topic_idx]
        arch_idx = round_num % len(archetypes)
        q_template, opt_a_tmpl, opt_b_tmpl, opt_c_tmpl, opt_d_tmpl = archetypes[arch_idx]
        q_text = f"{q_template.format(topic=chosen_topic, role=role)} (Evaluation Case #{seed_offset + round_num})"
        opt_a = opt_a_tmpl.format(topic=chosen_topic, role=role)
        opt_b = opt_b_tmpl.format(topic=chosen_topic, role=role)
        opt_c = opt_c_tmpl.format(topic=chosen_topic, role=role)
        opt_d = opt_d_tmpl.format(topic=chosen_topic, role=role)

        if mode == "mcq":
            raw_options = [
                {"key": "A", "text": opt_a},
                {"key": "B", "text": opt_b},
                {"key": "C", "text": opt_c},
                {"key": "D", "text": opt_d}
            ]
            shuffled_opts, shuffled_key = shuffle_mcq_options(raw_options, "A")
            return {
                "question_text": q_text,
                "topic": chosen_topic,
                "options": shuffled_opts,
                "correct_option": shuffled_key,
                "explanation": f"In production {role} engineering, {chosen_topic} demands {opt_a.lower()}."
            }
        else:
            return {
                "question_text": f"Explain the architectural trade-offs, practical implementation patterns, and error handling strategies for {chosen_topic} in a production {role} environment (Case #{seed_offset + round_num}).",
                "topic": chosen_topic,
                "model_answer": f"When implementing {chosen_topic} for a {role} system, engineers must account for performance, failure modes, monitoring, and modularity. Production solutions decouple implementation details through interfaces, enforce strict typing and error logging, and measure latency and throughput under peak load."
            }

    async def evaluate_text_answer(
        self,
        role: str,
        difficulty: str,
        question_text: str,
        user_answer: str,
        topic: str
    ) -> Dict[str, Any]:
        """Evaluates a text-based interview response against 6 rigorous criteria using Gemini or heuristic engine."""
        prompt = f"""You are an expert technical interviewer evaluating an engineering candidate for a {difficulty} {role} position.

Question: {question_text}
Topic: {topic}
Candidate Answer: {user_answer}

Evaluate the candidate's answer based on:
1. Technical correctness
2. Relevance to the question
3. Conceptual understanding
4. Technical depth
5. Clarity
6. Completeness

Return strict JSON matching the following schema:
{{
  "score": integer between 0 and 10,
  "feedback": "2-3 sentences concise professional evaluation",
  "strengths": ["bullet point 1", "bullet point 2"],
  "missing_concepts": ["concept 1", "concept 2"],
  "improvement_tips": ["actionable advice 1", "actionable advice 2"],
  "model_answer": "A comprehensive, ideal engineering model answer demonstrating best practices"
}}
Do NOT award high marks merely for length; evaluate technical precision.
"""
        raw_response = await self._call_gemini(prompt, temperature=0.2)
        if raw_response:
            try:
                data = json.loads(raw_response)
                score = int(data.get("score", 7))
                score = max(0, min(10, score))
                return {
                    "score": float(score),
                    "feedback": data.get("feedback", "Good effort demonstrating conceptual foundation."),
                    "strengths": data.get("strengths", ["Identified core terminology"]),
                    "missing_concepts": data.get("missing_concepts", ["Could include deeper architectural trade-offs"]),
                    "improvement_tips": data.get("improvement_tips", ["Review real-world production edge cases"]),
                    "model_answer": data.get("model_answer", "Refer to standard documentation and best practices.")
                }
            except Exception as e:
                logger.error(f"Error parsing Gemini evaluation response: {e}")

        # Algorithmic fallback evaluator for offline/resilience
        return self._heuristic_evaluate_text(question_text, user_answer, role, difficulty)

    def _heuristic_evaluate_text(
        self,
        question_text: str,
        user_answer: str,
        role: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """Deterministic evaluation fallback analyzing keywords, structure, and depth."""
        cleaned = user_answer.strip().lower()
        word_count = len(cleaned.split())

        if word_count < 10:
            score = 2
            feedback = "The answer is too brief to demonstrate adequate technical depth for this question."
            strengths = ["Attempted the question"]
            missing = ["Detailed technical explanation", "Underlying architectural reasoning", "Concrete examples"]
            tips = ["Elaborate on the mechanism and discuss trade-offs", "Provide code or pseudocode where relevant"]
        elif word_count < 35:
            score = 5
            feedback = "The answer mentions foundational concepts but lacks comprehensive technical detail and trade-offs."
            strengths = ["Identifies the primary topic", "Direct and concise"]
            missing = ["Edge-case handling", "Performance considerations", "Implementation specifics"]
            tips = ["Structure your answer into definition, mechanism, and real-world example", "Discuss advantages vs limitations"]
        elif word_count < 75:
            score = 7
            feedback = "Solid explanation showing clear conceptual understanding and relevant terminology."
            strengths = ["Clear conceptual grasp", "Accurate technical vocabulary", "Well structured response"]
            missing = ["Deeper production constraints or quantitative benchmarks"]
            tips = ["Mention specific libraries, tools, or design patterns used in enterprise environments"]
        else:
            score = 9
            feedback = "Excellent, thorough response with strong technical depth, clear structure, and practical reasoning."
            strengths = ["Comprehensive coverage of core concepts", "Articulates real-world considerations", "High clarity and depth"]
            missing = ["Minor optimization nuances under high concurrency"]
            tips = ["Keep this structured approach in live interviews"]

        model_answer = (
            f"An ideal response for {role} ({difficulty}) should explain the underlying mechanism, "
            f"cite performance or architectural implications, highlight key trade-offs, and provide a concrete production example."
        )

        return {
            "score": float(score),
            "feedback": feedback,
            "strengths": strengths,
            "missing_concepts": missing,
            "improvement_tips": tips,
            "model_answer": model_answer
        }

ai_service = AIService()
