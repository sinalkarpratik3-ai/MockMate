import re
import string
import random
import json
from typing import List, Dict, Any, Optional, Tuple

def shuffle_mcq_options(options: Any, correct_option: Optional[str]) -> Tuple[List[Dict[str, str]], str]:
    """
    Randomly shuffles MCQ options and re-keys them (A, B, C, D) while updating
    the correct_option key to match the new position of the correct answer.
    Guarantees equal random distribution across options A, B, C, D.
    """
    if not options:
        return [], "A"

    if isinstance(options, str):
        try:
            options_list = json.loads(options)
        except Exception:
            return options, correct_option or "A"
    elif isinstance(options, list):
        options_list = [dict(opt) if isinstance(opt, dict) else {"text": str(opt)} for opt in options]
    else:
        return options, correct_option or "A"

    if len(options_list) < 2:
        return options_list, correct_option or "A"

    target_key = (correct_option or "A").strip().upper()

    # Locate the correct option item
    correct_item = None
    for opt in options_list:
        if str(opt.get("key", "")).strip().upper() == target_key:
            correct_item = opt
            break

    if correct_item is None and options_list:
        correct_item = options_list[0]

    # Tag each item so we know which one was correct regardless of text collisions
    tagged = []
    for opt in options_list:
        tagged.append({
            "text": opt.get("text", "") if isinstance(opt, dict) else str(opt),
            "is_correct": (opt is correct_item)
        })

    # Shuffle the options randomly
    random.shuffle(tagged)

    # Re-assign standard keys A, B, C, D...
    keys = ["A", "B", "C", "D", "E", "F"]
    new_options = []
    new_correct_key = "A"

    for idx, item in enumerate(tagged):
        k = keys[idx] if idx < len(keys) else chr(65 + idx)
        new_options.append({"key": k, "text": item["text"]})
        if item["is_correct"]:
            new_correct_key = k

    return new_options, new_correct_key

# ==============================================================================
# 1. TEXT NORMALIZATION & NEAR-DUPLICATE DETECTION
# ==============================================================================

def normalize_question_text(text: str) -> str:
    """
    Normalizes question text to prevent duplicates and near-duplicates:
    - Strips code blocks, backticks, quotes, markdown formatting
    - Converts to lowercase
    - Strips common framing prefixes ("what is", "explain how", "describe", etc.)
    - Removes punctuation and normalizes whitespace
    """
    if not text:
        return ""
    # Strip markdown code blocks and inline code
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    cleaned = re.sub(r"[`*_~\"\'\(\)\[\]\{\}]", "", cleaned)
    cleaned = cleaned.lower().strip()

    # Strip conversational prefixes
    cleaned = re.sub(
        r"^(what is|what are|explain|describe|can you explain|how does|how do|how would you|"
        r"in python,?|in java,?|in javascript,?|in react,?|in sql,?|in docker,?)\s+",
        "",
        cleaned,
    )

    # Replace punctuation with spaces
    cleaned = cleaned.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    tokens = [w for w in cleaned.split() if len(w) > 1]
    return " ".join(tokens)


def is_duplicate_or_near_duplicate(
    candidate: str,
    existing_list: List[str],
    threshold: float = 0.65
) -> bool:
    """
    Checks if a candidate question is an exact match or near-duplicate (token similarity >= threshold)
    against any question in existing_list.
    """
    cand_norm = normalize_question_text(candidate)
    if not cand_norm:
        return False

    cand_tokens = set(cand_norm.split())
    if not cand_tokens:
        return False

    for existing in existing_list:
        if not existing:
            continue
        ex_norm = normalize_question_text(existing)
        if not ex_norm:
            continue

        # Exact normalized match
        if cand_norm == ex_norm:
            return True

        ex_tokens = set(ex_norm.split())
        if not ex_tokens:
            continue

        # Token similarity (Jaccard) and overlap coefficient (Szymkiewicz-Simpson)
        intersection = cand_tokens.intersection(ex_tokens)
        union = cand_tokens.union(ex_tokens)
        min_tokens = min(len(cand_tokens), len(ex_tokens))

        if union:
            sim = len(intersection) / len(union)
            if sim >= threshold:
                return True

        if min_tokens > 0:
            overlap = len(intersection) / min_tokens
            # If at least 80% of the shorter question's content words are shared with at least 5 intersecting tokens
            if overlap >= 0.80 and len(intersection) >= 5:
                return True

        # Substring containment only if the shorter question constitutes >= 85% of the longer question
        if len(cand_norm) > 30 and len(ex_norm) > 30:
            shorter_len = min(len(cand_norm), len(ex_norm))
            longer_len = max(len(cand_norm), len(ex_norm))
            if (cand_norm in ex_norm or ex_norm in cand_norm) and (shorter_len / longer_len >= 0.85):
                return True

    return False


# ==============================================================================
# 2. PROGRESSIVE & ADAPTIVE DIFFICULTY RULES
# ==============================================================================

DIFFICULTY_PROGRESSION = [
    "Easy",             # Round 1: Definitions, syntax, fundamental concepts
    "Easy to Medium",   # Round 2: Practical applications, simple problem-solving
    "Medium",           # Round 3: Applied knowledge, multi-step scenarios, trade-offs
    "Medium to Hard",   # Round 4: Debugging, optimization, architectural decisions
    "Hard"              # Round 5: Advanced concepts, system design, edge cases
]

def get_round_difficulty(round_number: int, total_rounds: int = 5) -> str:
    """
    Returns the target progressive difficulty for a given round number.
    Round 1 ALWAYS starts with Easy.
    """
    if total_rounds <= 1:
        return "Easy"
    
    # Scale round_number (1-indexed) into difficulty index (0 to 4)
    idx = min(round_number - 1, len(DIFFICULTY_PROGRESSION) - 1)
    if idx < 0:
        idx = 0
    return DIFFICULTY_PROGRESSION[idx]


def adapt_difficulty(current_difficulty: str, score_pct: Optional[float] = None, score_percentage: Optional[float] = None) -> str:
    """
    Adaptively adjusts difficulty for the next round based on user performance:
    - If user struggled severely (< 35% score): steps down 2 levels to solidify fundamentals.
    - If user struggled moderately (< 50% score): steps down 1 level to intermediate difficulty.
    - If user excelled (>= 80% score): smoothly advances difficulty.
    - If user performed moderately (50-79%): maintains current difficulty tier.
    """
    pct = score_pct if score_pct is not None else (score_percentage if score_percentage is not None else 50.0)
    levels = ["Easy", "Easy to Medium", "Medium", "Medium to Hard", "Hard"]
    try:
        curr_idx = levels.index(current_difficulty)
    except ValueError:
        curr_idx = 2  # default Medium

    if pct < 30.0:
        # Struggled severely: step down 2 levels to reinforce prerequisites
        new_idx = max(0, curr_idx - 2)
    elif pct < 50.0:
        # Struggled moderately: step down 1 level to intermediate
        new_idx = max(0, curr_idx - 1)
    elif pct >= 80.0:
        # Excelled: step up
        new_idx = min(len(levels) - 1, curr_idx + 1)
    else:
        # Moderate performance: maintain current pace
        new_idx = curr_idx

    return levels[new_idx]


# ==============================================================================
# 3. DOMAIN TOPIC TAXONOMY
# ==============================================================================

ROLE_TOPICS: Dict[str, List[str]] = {
    "Python Developer": [
        "Python Data Types & Collections", "Decorators & Generators", "GIL & Multithreading vs Multiprocessing",
        "Memory Management & Reference Counting", "Object-Oriented Python & Dunder Methods",
        "Asyncio & Cooperative Multitasking", "Context Managers (__enter__/__exit__)",
        "Metaclasses & Dynamic Attributes", "Exception Hierarchy & Handling", "Standard Library & Collections"
    ],
    "Java Developer": [
        "Core Java OOP & Polymorphism", "Java Collections Framework & Internals", "JVM Memory Model & Garbage Collection",
        "Java Concurrency & Multi-threading", "Spring Boot & Dependency Injection", "Hibernate & JPA Persistence",
        "Exception Handling (Checked vs Unchecked)", "Java Generics & Type Erasure", "Design Patterns in Java",
        "Microservices with Spring Cloud"
    ],
    "Web Developer": [
        "HTML5 Semantics & Accessibility (WCAG)", "CSS Architecture, Flexbox & Grid", "JavaScript ES6+ & DOM Manipulation",
        "HTTP/HTTPS Protocols & Status Codes", "RESTful API Integration & Fetch", "Client-Side Routing & Single Page Apps",
        "Browser Storage (Cookies, LocalStorage, IndexedDB)", "Web Performance & Asset Optimization",
        "Frontend Security (XSS, CSRF & CSP)", "Responsive Design & Mobile-First"
    ],
    "Frontend Developer": [
        "React Hooks & Component Lifecycle", "Modern CSS (Flexbox, Grid & Container Queries)",
        "Core Web Vitals & Web Performance", "JavaScript Event Loop & Microtasks",
        "Web Accessibility (ARIA & Focus Control)", "TypeScript Generics & Discriminated Unions",
        "Web Workers & Off-Main-Thread Processing", "Frontend Security (XSS, CSRF & CSP)",
        "State Management Architecture (Redux/Zustand)", "Critical Rendering Path & Bundle Splitting"
    ],
    "Backend Developer": [
        "REST API Design & Idempotency", "Database Indexing (B-Tree, Hash, GIN) & Query Plans",
        "Distributed Caching Strategies & Redis", "SQL Transaction Isolation Levels & ACID",
        "API Rate Limiting & Token Bucket Algorithms", "Microservices Communication (gRPC vs REST)",
        "Message Queues (Kafka / RabbitMQ)", "Authentication, JWT Security & Refresh Rotation",
        "Database Sharding & Read Replicas", "System Resilience (Circuit Breaker & Fallback)"
    ],
    "Data Analyst": [
        "SQL Window Functions & Aggregations", "Data Cleaning & Missing Value Imputation",
        "Statistical Outlier Detection & Anomaly Filtering", "Star Schema vs Snowflake Data Modeling",
        "A/B Testing, Hypothesis Testing & P-Values", "Cohort Retention Analysis & Churn Modeling",
        "Data Visualization & Cognitive Load", "Common Table Expressions (CTEs) vs Views",
        "Exploratory Data Analysis with Pandas", "Sampling Bias, Survivorship Bias & Simpson's Paradox"
    ],
    "Machine Learning Engineer": [
        "Supervised vs Unsupervised Learning Algorithms", "Feature Engineering & Dimensionality Reduction (PCA)",
        "Bias-Variance Tradeoff & Regularization (L1/L2)", "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
        "Gradient Descent & Optimization (Adam, SGD)", "Neural Network Architectures & Backpropagation",
        "Handling Class Imbalance (SMOTE, Focal Loss)", "Ensemble Learning (Random Forest, XGBoost)",
        "Model Deployment & Inference Latency Optimization", "Data Drift, Concept Drift & Model Monitoring"
    ],
    "Database Administrator": [
        "Relational Schema Design & 3NF Normalization", "B-Tree vs Hash vs Bitmap Index Architecture",
        "ACID Properties & Write-Ahead Logging (WAL)", "Query Execution Plans & EXPLAIN ANALYZE",
        "Locking Mechanisms & Deadlock Resolution", "Backup Strategies, Point-in-Time Recovery (PITR)",
        "Database Replication (Synchronous vs Asynchronous)", "Table Partitioning & Sharding Techniques",
        "Connection Pooling & Resource Limits", "Database Security, Role-Based Access & Encryption"
    ],
    "Computer Networks": [
        "OSI Model vs TCP/IP Protocol Suite", "TCP 3-Way Handshake, Flow Control & Congestion Control",
        "UDP vs TCP Protocol Characteristics", "DNS Resolution Architecture & Record Types",
        "Subnetting, CIDR & IP Addressing", "Routing Protocols (BGP, OSPF, RIP)",
        "HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)", "Network Address Translation (NAT) & PAT",
        "TLS/SSL Handshake & Symmetric/Asymmetric Encryption", "VLANs, Switching & Spanning Tree Protocol (STP)"
    ],
    "DevOps Engineer": [
        "Docker Containerization & Multi-stage Builds", "Kubernetes Pods, Deployments & DaemonSets",
        "CI/CD Pipelines & GitHub Actions Workflows", "Infrastructure as Code (Terraform & State Locking)",
        "Observability & Monitoring (Prometheus & Grafana)", "Zero-Downtime Deployments (Blue-Green & Canary)",
        "Linux Systems Administration & Shell Scripting", "GitOps Principles & ArgoCD",
        "Cloud Networking (VPC, Subnets, Security Groups)", "Secret Management (HashiCorp Vault & AWS Secrets)"
    ]
}

def get_topics_for_role(role: str) -> List[str]:
    """
    Returns verified topic focus areas for any role.
    If the role is not pre-registered, dynamically generates high-quality domain topics.
    """
    for registered_role, topics in ROLE_TOPICS.items():
        if role.strip().lower() == registered_role.lower() or registered_role.lower() in role.strip().lower():
            return topics

    # Dynamic domain topic generation for any unlisted technical domain
    clean_role = role.strip()
    return [
        f"{clean_role} Core Fundamentals & Architecture",
        f"{clean_role} Best Practices & Design Patterns",
        f"{clean_role} Performance Optimization & Scalability",
        f"{clean_role} Error Handling, Debugging & Reliability",
        f"{clean_role} Security, Authentication & Access Control",
        f"{clean_role} Testing, Validation & Quality Assurance",
        f"{clean_role} Tooling, Ecosystem & Modern Frameworks",
        f"{clean_role} System Design & Production Trade-offs"
    ]


# ==============================================================================
# 4. COMPREHENSIVE MULTI-TIER FALLBACK QUESTION BANKS (MCQ & TEXT)
# ==============================================================================

# Structure: ROLE -> DIFFICULTY -> List of questions
FALLBACK_MCQ_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Python Developer": {
        "Easy": [
            {
                "question_text": "In Python, which built-in data type is immutable?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "tuple"},
                    {"key": "B", "text": "list"},
                    {"key": "C", "text": "dict"},
                    {"key": "D", "text": "set"}
                ],
                "correct_option": "A",
                "explanation": "Tuples are immutable sequence types in Python; once defined, their elements cannot be added, removed, or reassigned."
            },
            {
                "question_text": "What does the `len()` function return when called on an empty dictionary?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "0"},
                    {"key": "B", "text": "None"},
                    {"key": "C", "text": "TypeError"},
                    {"key": "D", "text": "1"}
                ],
                "correct_option": "A",
                "explanation": "Calling len() on any empty container in Python (including dicts, lists, and sets) returns 0."
            },
            {
                "question_text": "How does accessing a dictionary key using `dict.get('key', default)` differ from `dict['key']`?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "`dict.get()` returns the default value if the key is missing, while `dict['key']` raises a `KeyError`"},
                    {"key": "B", "text": "`dict['key']` automatically inserts the missing key with None"},
                    {"key": "C", "text": "`dict.get()` deletes the key after reading it"},
                    {"key": "D", "text": "`dict.get()` is only valid for integer keys"}
                ],
                "correct_option": "A",
                "explanation": "`dict.get(key, default)` safely retrieves the value or returns default (or None) without raising KeyError when the key does not exist."
            },
            {
                "question_text": "What does the slice expression `text[1:5]` return given `text = 'PYTHON'`?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "'YTHO'"},
                    {"key": "B", "text": "'PYTH'"},
                    {"key": "C", "text": "'YTHON'"},
                    {"key": "D", "text": "'PYTHON'"}
                ],
                "correct_option": "A",
                "explanation": "Slicing is zero-indexed and exclusive of the end index: index 1 is 'Y', index 4 is 'O', yielding 'YTHO'."
            },
            {
                "question_text": "What is the key difference between `list.append(x)` and `list.extend(x)` in Python?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "`append` adds `x` as a single element, while `extend` iterates over `x` and adds each of its items"},
                    {"key": "B", "text": "`extend` can only be called on tuples"},
                    {"key": "C", "text": "`append` creates a new list copy, while `extend` operates in-place"},
                    {"key": "D", "text": "`extend` sorts the list automatically after insertion"}
                ],
                "correct_option": "A",
                "explanation": "`append(x)` adds object `x` directly to the end of the list as one element. `extend(iterable)` iterates through the argument, appending each item individually."
            },
            {
                "question_text": "In a Python `if` statement, how do empty containers like `[]`, `{}`, and `''` evaluate?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "They evaluate to `False` in a boolean context"},
                    {"key": "B", "text": "They raise an `EmptyContainerException`"},
                    {"key": "C", "text": "They evaluate to `True` because the container object exists"},
                    {"key": "D", "text": "They evaluate to `None`"}
                ],
                "correct_option": "A",
                "explanation": "In Python's truth-value testing, empty sequences and collections (`[]`, `{}`, `set()`, `''`, `()`, `0`) evaluate to `False`."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the primary difference in behavior between `is` and `==` in Python?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "`is` checks object memory identity, while `==` checks value equality"},
                    {"key": "B", "text": "`is` checks variable data type, while `==` checks memory address"},
                    {"key": "C", "text": "`==` is only used for strings, while `is` is used for numbers"},
                    {"key": "D", "text": "`is` converts objects to integers before comparing"}
                ],
                "correct_option": "A",
                "explanation": "`is` verifies whether two identifiers point to the identical memory address (id(a) == id(b)), whereas `==` evaluates value equality via __eq__."
            },
            {
                "question_text": "What protocol must an object implement to be used as a context manager with Python's `with` statement?",
                "topic": "Context Managers (__enter__/__exit__)",
                "options": [
                    {"key": "A", "text": "__enter__() and __exit__() methods"},
                    {"key": "B", "text": "__open__() and __close__() methods"},
                    {"key": "C", "text": "__start__() and __stop__() methods"},
                    {"key": "D", "text": "__iter__() and __next__() methods"}
                ],
                "correct_option": "A",
                "explanation": "Python's context management protocol requires the __enter__() and __exit__() dunder methods."
            },
            {
                "question_text": "What is the purpose of `*args` and `**kwargs` in a Python function definition?",
                "topic": "Functions & Variable Scope",
                "options": [
                    {"key": "A", "text": "`*args` collects positional arguments into a tuple, while `**kwargs` collects keyword arguments into a dictionary"},
                    {"key": "B", "text": "`*args` enforces static typing, while `**kwargs` allows global variable access"},
                    {"key": "C", "text": "`*args` compiles the function to C bytecode"},
                    {"key": "D", "text": "`**kwargs` is required for all recursive function definitions"}
                ],
                "correct_option": "A",
                "explanation": "`*args` enables a function to accept any number of positional arguments unpacked into a tuple, and `**kwargs` accepts arbitrary keyword arguments as a dictionary."
            },
            {
                "question_text": "What does Python's built-in `enumerate(iterable, start=0)` function yield on each iteration?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "A tuple containing `(current_index, item)`"},
                    {"key": "B", "text": "Only the integer index of the item"},
                    {"key": "C", "text": "A reversed copy of the iterable"},
                    {"key": "D", "text": "A dictionary mapping all keys to values"}
                ],
                "correct_option": "A",
                "explanation": "`enumerate()` takes an iterable and returns an enumerate object that yields pairs of `(count, value)` on each iteration."
            },
            {
                "question_text": "In a `try...except...else...finally` block, when does the `else` clause execute?",
                "topic": "Error Handling & Debugging",
                "options": [
                    {"key": "A", "text": "Only when the `try` block completes without raising any exception"},
                    {"key": "B", "text": "Whenever an unhandled exception occurs"},
                    {"key": "C", "text": "Always immediately before the `finally` block"},
                    {"key": "D", "text": "Only when the `finally` block raises an error"}
                ],
                "correct_option": "A",
                "explanation": "The `else` clause in exception handling runs if and only if the code in the `try` clause did not raise an exception."
            }
        ],
        "Medium": [
            {
                "question_text": "What is the key behavioral difference between a standard function and a generator function containing `yield`?",
                "topic": "Decorators & Generators",
                "options": [
                    {"key": "A", "text": "Generators pause execution and yield values lazily, preserving their stack frame state"},
                    {"key": "B", "text": "Generators run in separate OS threads automatically"},
                    {"key": "C", "text": "Generators can only return string objects"},
                    {"key": "D", "text": "Generators convert all variables into global constants"}
                ],
                "correct_option": "A",
                "explanation": "A generator returns an iterator that pauses at each yield statement, keeping local variable state suspended until the next item is requested."
            },
            {
                "question_text": "Why should mutable objects (like `[]` or `{}`) generally be avoided as default argument values in Python functions?",
                "topic": "Python Data Types & Collections",
                "options": [
                    {"key": "A", "text": "Default arguments are evaluated once at definition time, so mutations persist across all subsequent function calls"},
                    {"key": "B", "text": "Python raises a SyntaxError at compile time"},
                    {"key": "C", "text": "Mutable defaults are immediately garbage collected after the first call"},
                    {"key": "D", "text": "Python converts mutable defaults into immutable strings"}
                ],
                "correct_option": "A",
                "explanation": "Default parameter values are instantiated when the function is defined, sharing the exact same object instance across every call that relies on the default."
            },
            {
                "question_text": "What is the difference between `copy.copy()` (shallow copy) and `copy.deepcopy()` in Python?",
                "topic": "Memory Management & Reference Counting",
                "options": [
                    {"key": "A", "text": "Shallow copy creates a new container but inserts references to the original child objects; deep copy recursively copies child objects"},
                    {"key": "B", "text": "Shallow copy only works on primitive types, while deep copy converts objects into JSON strings"},
                    {"key": "C", "text": "Deep copy deletes the original object from RAM after copying"},
                    {"key": "D", "text": "Shallow copy creates thread-safe locks around attributes"}
                ],
                "correct_option": "A",
                "explanation": "A shallow copy constructs a new collection object and populates it with references to child items. A deep copy recursively duplicates every object found within the original hierarchy."
            },
            {
                "question_text": "Why should `@functools.wraps(func)` be used when implementing a custom Python decorator?",
                "topic": "Decorators & Generators",
                "options": [
                    {"key": "A", "text": "It preserves the original function's docstring, name, module, and signature on the wrapper"},
                    {"key": "B", "text": "It compiles the decorator wrapper into native C machine code"},
                    {"key": "C", "text": "It forces the decorated function to run in a background daemon thread"},
                    {"key": "D", "text": "It bypasses Python's maximum recursion limit"}
                ],
                "correct_option": "A",
                "explanation": "`functools.wraps` copies metadata (such as `__name__`, `__doc__`, and `__annotations__`) from the decorated function onto the wrapper function, preventing introspection breakdown."
            },
            {
                "question_text": "What is the primary advantage of using `isinstance(obj, Class)` over `type(obj) is Class` for type checking?",
                "topic": "Object-Oriented Python",
                "options": [
                    {"key": "A", "text": "`isinstance()` correctly considers subclass inheritance, whereas `type() is` only checks exact class identity"},
                    {"key": "B", "text": "`isinstance()` executes twice as fast as `type()`"},
                    {"key": "C", "text": "`type() is` fails if the object has more than two attributes"},
                    {"key": "D", "text": "`isinstance()` converts instances to dictionaries"}
                ],
                "correct_option": "A",
                "explanation": "`isinstance()` supports inheritance hierarchies by returning True if `obj` is an instance of `Class` or any subclass derived from it."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "How does the Global Interpreter Lock (GIL) in CPython affect multi-threaded CPU-bound programs?",
                "topic": "GIL & Multithreading vs Multiprocessing",
                "options": [
                    {"key": "A", "text": "It restricts execution to one native thread running Python bytecode at a time, preventing CPU-bound scaling"},
                    {"key": "B", "text": "It prevents threads from performing I/O bound network requests"},
                    {"key": "C", "text": "It forces all threads to allocate memory from the OS kernel stack"},
                    {"key": "D", "text": "It automatically converts recursive algorithms to iterative loops"}
                ],
                "correct_option": "A",
                "explanation": "The CPython GIL ensures thread safety by permitting only one thread to execute Python bytecode at any instant, meaning CPU-bound concurrency requires multiprocessing."
            },
            {
                "question_text": "What is the primary memory optimization achieved by specifying `__slots__` in a Python class?",
                "topic": "Memory Management & Reference Counting",
                "options": [
                    {"key": "A", "text": "It suppresses the creation of the dynamic `__dict__` dictionary per instance, significantly saving RAM"},
                    {"key": "B", "text": "It enables asynchronous bytecode compilation"},
                    {"key": "C", "text": "It automatically compresses numeric attributes using gzip"},
                    {"key": "D", "text": "It disables reference counting for the class"}
                ],
                "correct_option": "A",
                "explanation": "Defining __slots__ allocates space for a fixed tuple of attributes rather than creating a dynamic __dict__ for every object, dramatically reducing memory overhead."
            },
            {
                "question_text": "In Python's `asyncio` framework, what occurs when an `await` expression is reached inside a coroutine?",
                "topic": "Asynchronous Programming (asyncio)",
                "options": [
                    {"key": "A", "text": "Execution of that coroutine suspends, yielding control back to the event loop to run other scheduled tasks"},
                    {"key": "B", "text": "A new OS thread is spawned to run the awaited target synchronously"},
                    {"key": "C", "text": "The entire Python process blocks until the target completes"},
                    {"key": "D", "text": "Python executes a full garbage collection sweep"}
                ],
                "correct_option": "A",
                "explanation": "`await` cooperative suspension transfers control back to the asyncio event loop, allowing other concurrent coroutines or I/O callbacks to make progress."
            },
            {
                "question_text": "What distinction characterizes `@classmethod` compared to `@staticmethod` in Python class definitions?",
                "topic": "Object-Oriented Python",
                "options": [
                    {"key": "A", "text": "`@classmethod` receives the class (`cls`) as its first argument; `@staticmethod` receives no implicit class or instance argument"},
                    {"key": "B", "text": "`@staticmethod` can only access private attributes beginning with double underscore"},
                    {"key": "C", "text": "`@classmethod` can only be invoked on subclasses, never the base class"},
                    {"key": "D", "text": "`@staticmethod` runs synchronously while `@classmethod` is always async"}
                ],
                "correct_option": "A",
                "explanation": "Methods decorated with `@classmethod` take the class object `cls` as the first argument, enabling alternative constructors and inheritance awareness. `@staticmethod` behaves like a plain function placed inside the class namespace."
            }
        ],
        "Hard": [
            {
                "question_text": "In CPython's generational cyclic garbage collector, how are circular reference graphs resolved?",
                "topic": "Memory Management & Reference Counting",
                "options": [
                    {"key": "A", "text": "By traversing PyObject pointer references across Generations 0, 1, and 2 to identify unreachable isolated subgraphs"},
                    {"key": "B", "text": "By immediately terminating any process that instantiates circular references"},
                    {"key": "C", "text": "By executing a full memory compaction cycle on every function return"},
                    {"key": "D", "text": "By converting circular references into weakref proxies automatically"}
                ],
                "correct_option": "A",
                "explanation": "CPython uses a generational cyclic garbage collector that tracks container objects across three generations, detecting unreachable isolated clusters whose reference count is greater than zero."
            },
            {
                "question_text": "When defining a custom metaclass in Python (`class Meta(type):`), what is the primary role of the `__new__` method?",
                "topic": "Metaprogramming & Advanced Python",
                "options": [
                    {"key": "A", "text": "It constructs and allocates the actual class object itself before the class body is initialized"},
                    {"key": "B", "text": "It instantiates individual instances of the class at runtime"},
                    {"key": "C", "text": "It registers the class with the operating system dynamic linker"},
                    {"key": "D", "text": "It encrypts the class methods into binary bytecode"}
                ],
                "correct_option": "A",
                "explanation": "In a metaclass, `__new__(mcs, name, bases, namespace)` is invoked to allocate and return the newly formed class type object before `__init__` configures it."
            },
            {
                "question_text": "What methods must an object implement to act as a custom Descriptor in Python, controlling attribute access on owner classes?",
                "topic": "Object-Oriented Python",
                "options": [
                    {"key": "A", "text": "At least one of `__get__()`, `__set__()`, or `__delete__()`"},
                    {"key": "B", "text": "`__read__()` and `__write__()`"},
                    {"key": "C", "text": "`__getattr__()` and `__setattr__()` only"},
                    {"key": "D", "text": "`__lock__()` and `__unlock__()`"}
                ],
                "correct_option": "A",
                "explanation": "The descriptor protocol consists of `__get__(self, instance, owner)`, `__set__(self, instance, value)`, and `__delete__(self, instance)`. Implementing any of these defines a descriptor."
            }
        ]
    },
    "Java Developer": {
        "Easy": [
            {
                "question_text": "In Java, what is the default value of an uninitialized instance variable of type `boolean`?",
                "topic": "Core Java OOP & Polymorphism",
                "options": [
                    {"key": "A", "text": "false"},
                    {"key": "B", "text": "true"},
                    {"key": "C", "text": "null"},
                    {"key": "D", "text": "0"}
                ],
                "correct_option": "A",
                "explanation": "In Java, uninitialized instance variables of primitive boolean type default to false."
            },
            {
                "question_text": "Which Java keyword is used by a subclass to call a constructor in its parent class?",
                "topic": "Core Java OOP & Polymorphism",
                "options": [
                    {"key": "A", "text": "super()"},
                    {"key": "B", "text": "this()"},
                    {"key": "C", "text": "parent()"},
                    {"key": "D", "text": "base()"}
                ],
                "correct_option": "A",
                "explanation": "The super() keyword invokes the constructor of the superclass from within a subclass constructor."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the primary difference between `ArrayList` and `LinkedList` in Java?",
                "topic": "Java Collections Framework & Internals",
                "options": [
                    {"key": "A", "text": "ArrayList uses a dynamic array providing O(1) random access; LinkedList uses nodes with O(1) insertions at ends"},
                    {"key": "B", "text": "ArrayList is thread-safe while LinkedList is not"},
                    {"key": "C", "text": "LinkedList can only store primitive integers"},
                    {"key": "D", "text": "ArrayList does not support duplicate elements"}
                ],
                "correct_option": "A",
                "explanation": "ArrayList provides fast O(1) random index lookups backed by a contiguous array, whereas LinkedList provides O(1) insertions/deletions at endpoints via pointer manipulation."
            }
        ],
        "Medium": [
            {
                "question_text": "What does the `volatile` keyword guarantee in multi-threaded Java applications?",
                "topic": "Java Concurrency & Multi-threading",
                "options": [
                    {"key": "A", "text": "Visibility of writes across all threads (main memory reads/writes) and prevents instruction reordering"},
                    {"key": "B", "text": "Atomic execution of compound statements like count++"},
                    {"key": "C", "text": "Exclusive synchronized locking for all methods"},
                    {"key": "D", "text": "Prevention of garbage collection on the variable"}
                ],
                "correct_option": "A",
                "explanation": "volatile establishes a happens-before relationship ensuring memory visibility across threads, but does not provide mutual exclusion for non-atomic operations."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In Java 8+, how does `HashMap` optimize performance when a single bucket experiences severe hash collisions?",
                "topic": "Java Collections Framework & Internals",
                "options": [
                    {"key": "A", "text": "It converts the bucket's LinkedList into a balanced Red-Black Tree once threshold (8) is exceeded"},
                    {"key": "B", "text": "It immediately drops colliding entries"},
                    {"key": "C", "text": "It switches the entire table to a ConcurrentSkipListMap"},
                    {"key": "D", "text": "It halts the JVM with a ConcurrentModificationException"}
                ],
                "correct_option": "A",
                "explanation": "Java 8 replaces bucket linked lists with balanced Red-Black trees when bucket size reaches TREEIFY_THRESHOLD (8), improving worst-case search time from O(n) to O(log n)."
            }
        ],
        "Hard": [
            {
                "question_text": "In the JVM, how does the G1 (Garbage-First) collector achieve predictable pause times compared to older CMS collectors?",
                "topic": "JVM Memory Model & Garbage Collection",
                "options": [
                    {"key": "A", "text": "By partitioning the heap into equal-sized regions and prioritizing collection of regions with the most reclaimable garbage"},
                    {"key": "B", "text": "By completely disabling Stop-The-World pause phases"},
                    {"key": "C", "text": "By compiling all Java bytecode directly to C++ pointers"},
                    {"key": "D", "text": "By running garbage collection exclusively on GPU hardware"}
                ],
                "correct_option": "A",
                "explanation": "G1 divides the heap into homogeneous regions and constructs a collection set prioritizing regions with the highest garbage density within a user-specified pause time target."
            }
        ]
    },
    "Frontend Developer": {
        "Easy": [
            {
                "question_text": "Which HTML element is the semantic standard for defining navigational links?",
                "topic": "HTML5 Semantics & Accessibility (WCAG)",
                "options": [
                    {"key": "A", "text": "<nav>"},
                    {"key": "B", "text": "<header>"},
                    {"key": "C", "text": "<navigate>"},
                    {"key": "D", "text": "<links>"}
                ],
                "correct_option": "A",
                "explanation": "The semantic <nav> tag represents a section of a page whose purpose is to provide navigation links."
            },
            {
                "question_text": "In CSS, which display value lays out child elements along a single flexible axis (row or column)?",
                "topic": "Modern CSS (Flexbox, Grid & Container Queries)",
                "options": [
                    {"key": "A", "text": "display: flex"},
                    {"key": "B", "text": "display: block"},
                    {"key": "C", "text": "display: inline"},
                    {"key": "D", "text": "display: table"}
                ],
                "correct_option": "A",
                "explanation": "Flexbox (display: flex) establishes a flexible 1-dimensional layout context."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "In React, what is the primary purpose of passing a unique `key` prop when rendering a dynamic list of items?",
                "topic": "React Hooks & Component Lifecycle",
                "options": [
                    {"key": "A", "text": "To help React reconcile DOM nodes efficiently during diffing and preserve component identity"},
                    {"key": "B", "text": "To apply unique CSS styles to every list row"},
                    {"key": "C", "text": "To automatically sort items in ascending order"},
                    {"key": "D", "text": "To enable Redux caching for the array"}
                ],
                "correct_option": "A",
                "explanation": "Stable keys allow React's reconciliation engine to identify which items have changed, moved, or been deleted without re-rendering the entire list."
            }
        ],
        "Medium": [
            {
                "question_text": "In modern web browsers, how does the Event Loop handle the microtask queue relative to macrotasks (like setTimeout)?",
                "topic": "JavaScript Event Loop & Microtasks",
                "options": [
                    {"key": "A", "text": "The entire microtask queue is completely drained after each execution task before the next macrotask runs"},
                    {"key": "B", "text": "Macrotasks always preempt microtasks when timers expire"},
                    {"key": "C", "text": "Microtasks and macrotasks execute concurrently in worker threads"},
                    {"key": "D", "text": "Microtasks run only once when the browser window closes"}
                ],
                "correct_option": "A",
                "explanation": "Microtasks (Promises, queueMicrotask) have strict priority; the event loop drains the entire microtask queue before picking the next task from the macrotask queue."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "What does Core Web Vital metric LCP (Largest Contentful Paint) specifically measure?",
                "topic": "Core Web Vitals & Web Performance",
                "options": [
                    {"key": "A", "text": "The time it takes for the largest visual content element in the viewport to finish rendering"},
                    {"key": "B", "text": "The total size in megabytes of all downloaded image files"},
                    {"key": "C", "text": "The responsiveness of the page to the initial mouse click"},
                    {"key": "D", "text": "The cumulative unexpected layout shifts during scrolling"}
                ],
                "correct_option": "A",
                "explanation": "LCP measures perceived load speed by recording when the main visual content element in the viewport (hero image, video banner, or large text block) has completed rendering."
            }
        ],
        "Hard": [
            {
                "question_text": "In React 18 Concurrent Mode, how does `useTransition` prevent UI jank during expensive state updates?",
                "topic": "React Hooks & Component Lifecycle",
                "options": [
                    {"key": "A", "text": "It marks state updates as non-urgent transitions, allowing React to interrupt rendering for urgent user input"},
                    {"key": "B", "text": "It moves DOM calculations directly into WebGL shader memory"},
                    {"key": "C", "text": "It disables component re-rendering entirely until the server responds"},
                    {"key": "D", "text": "It compiles JSX into native WebAssembly binaries"}
                ],
                "correct_option": "A",
                "explanation": "useTransition informs React that an update can be interrupted by higher-priority user events (such as typing into an input), keeping the interface responsive."
            }
        ]
    },
    "Backend Developer": {
        "Easy": [
            {
                "question_text": "Which HTTP status code signifies that a requested resource was successfully created on the server?",
                "topic": "REST API Design & Idempotency",
                "options": [
                    {"key": "A", "text": "201 Created"},
                    {"key": "B", "text": "200 OK"},
                    {"key": "C", "text": "204 No Content"},
                    {"key": "D", "text": "301 Moved Permanently"}
                ],
                "correct_option": "A",
                "explanation": "HTTP 201 Created indicates that the request succeeded and led to the creation of a new resource."
            },
            {
                "question_text": "Which SQL clause is used to filter records based on a specified condition?",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "options": [
                    {"key": "A", "text": "WHERE"},
                    {"key": "B", "text": "GROUP BY"},
                    {"key": "C", "text": "ORDER BY"},
                    {"key": "D", "text": "HAVING"}
                ],
                "correct_option": "A",
                "explanation": "The WHERE clause filters individual rows before any grouping or aggregation takes place."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Which HTTP method is required by the HTTP/1.1 specification to be idempotent?",
                "topic": "REST API Design & Idempotency",
                "options": [
                    {"key": "A", "text": "PUT"},
                    {"key": "B", "text": "POST"},
                    {"key": "C", "text": "PATCH (when appending values)"},
                    {"key": "D", "text": "CONNECT"}
                ],
                "correct_option": "A",
                "explanation": "PUT is idempotent: sending identical PUT requests multiple times results in the same server resource state as a single request."
            }
        ],
        "Medium": [
            {
                "question_text": "What is the primary advantage of storing user session state in Redis rather than inside web server process memory?",
                "topic": "Distributed Caching Strategies & Redis",
                "options": [
                    {"key": "A", "text": "It allows stateless web instances to scale horizontally behind a load balancer without sticky sessions"},
                    {"key": "B", "text": "It eliminates the need for database migrations entirely"},
                    {"key": "C", "text": "Redis automatically encrypts all passwords without hashing"},
                    {"key": "D", "text": "Process memory cannot exceed 1 MB"}
                ],
                "correct_option": "A",
                "explanation": "Centralized caching in Redis decouples session state from individual application instances, enabling horizontal autoscaling without session loss."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "What is the 'N+1 Query Problem' commonly encountered when using Object-Relational Mappers (ORMs)?",
                "topic": "Database Indexing (B-Tree, Hash, GIN) & Query Plans",
                "options": [
                    {"key": "A", "text": "Executing 1 query to fetch parent records, followed by N separate queries to load related child records"},
                    {"key": "B", "text": "Adding N columns to 1 table without a primary key"},
                    {"key": "C", "text": "Using N threads to execute 1 SQL transaction"},
                    {"key": "D", "text": "Creating N database connection pools on 1 server"}
                ],
                "correct_option": "A",
                "explanation": "The N+1 problem occurs when an application loads N parent entities and subsequently issues N separate queries for each parent's children instead of using a JOIN or batch fetch."
            }
        ],
        "Hard": [
            {
                "question_text": "In distributed microservices, how does the Saga pattern maintain data consistency across distributed databases?",
                "topic": "Microservices Communication (gRPC vs REST)",
                "options": [
                    {"key": "A", "text": "Through a sequence of local transactions where each step publishes events, with compensating transactions to roll back on failure"},
                    {"key": "B", "text": "By holding distributed two-phase commit locks across all databases indefinitely"},
                    {"key": "C", "text": "By forcing all microservices to connect to a single monolithic database"},
                    {"key": "D", "text": "By restarting backend containers whenever a query fails"}
                ],
                "correct_option": "A",
                "explanation": "The Saga pattern coordinates distributed transactions via sequential local transactions and compensating rollbacks, avoiding distributed blocking locks."
            }
        ]
    },
    "Data Analyst": {
        "Easy": [
            {
                "question_text": "In SQL, which aggregate function is used to calculate the arithmetic mean of a numeric column?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "AVG()"},
                    {"key": "B", "text": "MEAN()"},
                    {"key": "C", "text": "SUM()"},
                    {"key": "D", "text": "COUNT()"}
                ],
                "correct_option": "A",
                "explanation": "AVG() returns the average value of a numeric column in SQL."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "In SQL, what is the key difference between `WHERE` and `HAVING`?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "`WHERE` filters rows before grouping; `HAVING` filters aggregated groups after `GROUP BY`"},
                    {"key": "B", "text": "`HAVING` filters rows before `WHERE` executes"},
                    {"key": "C", "text": "`WHERE` can evaluate aggregate functions directly"},
                    {"key": "D", "text": "`HAVING` only works with integer primary keys"}
                ],
                "correct_option": "A",
                "explanation": "WHERE filters individual table rows prior to aggregation, while HAVING filters grouped results produced by GROUP BY."
            }
        ],
        "Medium": [
            {
                "question_text": "What is the primary difference between the `ROW_NUMBER()` and `RANK()` SQL window functions?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "ROW_NUMBER() assigns consecutive integers with no ties; RANK() assigns tied values identical rank and skips subsequent numbers"},
                    {"key": "B", "text": "RANK() does not support ORDER BY"},
                    {"key": "C", "text": "ROW_NUMBER() can only rank strings"},
                    {"key": "D", "text": "RANK() produces a dense sequence without gaps"}
                ],
                "correct_option": "A",
                "explanation": "ROW_NUMBER() always assigns strictly sequential numbers (1, 2, 3, 4). RANK() gives tied values identical rank and skips subsequent rank counts (e.g. 1, 2, 2, 4)."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In hypothesis testing, what does a p-value less than alpha (p < 0.05) indicate?",
                "topic": "A/B Testing, Hypothesis Testing & P-Values",
                "options": [
                    {"key": "A", "text": "There is statistically significant evidence to reject the null hypothesis in favor of the alternative hypothesis"},
                    {"key": "B", "text": "The null hypothesis is proven 100% true"},
                    {"key": "C", "text": "The sample size was too small to draw analytical conclusions"},
                    {"key": "D", "text": "The experiment must be restarted with different random seed"}
                ],
                "correct_option": "A",
                "explanation": "When p < alpha, the probability of observing the test result by random chance alone under the null hypothesis is below the threshold, warranting rejection of the null."
            }
        ],
        "Hard": [
            {
                "question_text": "In dimensional modeling, what is the architectural difference between a Star Schema and a Snowflake Schema?",
                "topic": "Star Schema vs Snowflake Data Modeling",
                "options": [
                    {"key": "A", "text": "In a Snowflake schema, dimension tables are normalized into multiple related tables; in a Star schema, dimension tables are denormalized"},
                    {"key": "B", "text": "Star schemas contain no fact tables"},
                    {"key": "C", "text": "Snowflake schemas only run on NoSQL databases"},
                    {"key": "D", "text": "Star schemas do not allow foreign key relationships"}
                ],
                "correct_option": "A",
                "explanation": "Star schemas maintain denormalized dimension tables directly connected to a central fact table for query speed. Snowflake schemas normalize dimension hierarchies into lookup tables."
            }
        ]
    },
    "Machine Learning Engineer": {
        "Easy": [
            {
                "question_text": "What type of machine learning task involves predicting a continuous numerical value?",
                "topic": "Supervised vs Unsupervised Learning Algorithms",
                "options": [
                    {"key": "A", "text": "Regression"},
                    {"key": "B", "text": "Classification"},
                    {"key": "C", "text": "Clustering"},
                    {"key": "D", "text": "Dimensionality Reduction"}
                ],
                "correct_option": "A",
                "explanation": "Regression tasks predict continuous numerical quantities (e.g., house prices, temperatures), whereas classification predicts discrete class labels."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What happens when a machine learning model exhibits high variance (overfitting)?",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "options": [
                    {"key": "A", "text": "It performs exceptionally well on training data but fails to generalize to unseen test data"},
                    {"key": "B", "text": "It has high training error and high test error"},
                    {"key": "C", "text": "It cannot learn non-linear decision boundaries"},
                    {"key": "D", "text": "It converges in zero iterations"}
                ],
                "correct_option": "A",
                "explanation": "High variance means the model has learned the training data noise rather than general patterns, resulting in near-perfect training accuracy but poor test generalization."
            }
        ],
        "Medium": [
            {
                "question_text": "When evaluating a classifier on an imbalanced dataset where positive cases are rare (1%), which metric is most informative?",
                "topic": "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
                "options": [
                    {"key": "A", "text": "Precision-Recall AUC (PR-AUC) or F1-Score"},
                    {"key": "B", "text": "Standard Accuracy"},
                    {"key": "C", "text": "Mean Squared Error (MSE)"},
                    {"key": "D", "text": "R-squared coefficient"}
                ],
                "correct_option": "A",
                "explanation": "Accuracy is misleading on imbalanced datasets (a dummy model predicting all negatives achieves 99% accuracy). PR-AUC and F1-Score focus on true positives and false positives/negatives."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "What is the mathematical difference between L1 (Lasso) and L2 (Ridge) regularization?",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "options": [
                    {"key": "A", "text": "L1 adds the absolute value of weights to the loss function, inducing sparse feature weights; L2 adds squared weights, shrinking them smoothly"},
                    {"key": "B", "text": "L2 produces exact zero weights while L1 does not"},
                    {"key": "C", "text": "L1 can only be applied to neural networks"},
                    {"key": "D", "text": "L2 regularization prevents gradient descent from running"}
                ],
                "correct_option": "A",
                "explanation": "L1 regularization penalizes the sum of absolute coefficients, driving unimportant weights to zero (feature selection). L2 penalizes squared weights, shrinking them toward zero without setting them exactly to zero."
            }
        ],
        "Hard": [
            {
                "question_text": "In transformer neural networks, why is the Scaled Dot-Product Attention divided by the square root of the key dimension (sqrt(d_k))?",
                "topic": "Neural Network Architectures & Backpropagation",
                "options": [
                    {"key": "A", "text": "To prevent large dot products from pushing the softmax function into regions with extremely small gradients"},
                    {"key": "B", "text": "To enforce binary attention masks across all layers"},
                    {"key": "C", "text": "To reduce matrix multiplication memory consumption by half"},
                    {"key": "D", "text": "To normalize token embeddings into ASCII characters"}
                ],
                "correct_option": "A",
                "explanation": "For large dimensions d_k, dot products grow large in magnitude, pushing softmax into saturated regions with vanishingly small gradients. Scaling by 1/sqrt(d_k) stabilizes the variance to 1."
            }
        ]
    },
    "Database Administrator": {
        "Easy": [
            {
                "question_text": "In relational databases, what does the primary key uniquely identify?",
                "topic": "Relational Schema Design & 3NF Normalization",
                "options": [
                    {"key": "A", "text": "Each unique record/row in a table"},
                    {"key": "B", "text": "The entire database file on disk"},
                    {"key": "C", "text": "The server hostname"},
                    {"key": "D", "text": "The SQL query execution time"}
                ],
                "correct_option": "A",
                "explanation": "A primary key constraint uniquely identifies each row in a database table, preventing duplicate records."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the primary purpose of database normalization up to Third Normal Form (3NF)?",
                "topic": "Relational Schema Design & 3NF Normalization",
                "options": [
                    {"key": "A", "text": "To eliminate data redundancy and prevent update, insert, and delete anomalies"},
                    {"key": "B", "text": "To increase table file sizes on disk"},
                    {"key": "C", "text": "To avoid using foreign key relationships"},
                    {"key": "D", "text": "To speed up full table scans"}
                ],
                "correct_option": "A",
                "explanation": "Normalization minimizes data duplication and prevents transitive dependencies, ensuring data integrity across modifications."
            }
        ],
        "Medium": [
            {
                "question_text": "In relational databases, what happens when a query performs an 'Index Scan' compared to a 'Sequential Scan'?",
                "topic": "B-Tree vs Hash vs Bitmap Index Architecture",
                "options": [
                    {"key": "A", "text": "An Index Scan reads the B-Tree index to locate row pointers in O(log N) time, avoiding reading the entire table"},
                    {"key": "B", "text": "An Index Scan locks the entire table during execution"},
                    {"key": "C", "text": "Sequential Scan is always faster for selective WHERE filters"},
                    {"key": "D", "text": "An Index Scan converts relational tables to unindexed text files"}
                ],
                "correct_option": "A",
                "explanation": "An index scan traverses the balanced tree structure to find matching row IDs in O(log N) time, whereas a sequential scan reads all disk blocks sequentially."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In ACID transactions, what anomaly does the 'Serializable' isolation level prevent that 'Repeatable Read' permits in some engines?",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "options": [
                    {"key": "A", "text": "Phantom Reads and Serialization Anomalies (such as Write Skew)"},
                    {"key": "B", "text": "Dirty Reads only"},
                    {"key": "C", "text": "Foreign Key constraints"},
                    {"key": "D", "text": "Primary Key generation"}
                ],
                "correct_option": "A",
                "explanation": "Serializable is the highest isolation level and guarantees transactions execute as if strictly serial, preventing phantom reads and write skew anomalies."
            }
        ],
        "Hard": [
            {
                "question_text": "How does Write-Ahead Logging (WAL) guarantee durability and atomicity in relational database engines (like PostgreSQL)?",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "options": [
                    {"key": "A", "text": "Changes are appended to persistent disk logs before data pages in memory are written to disk, enabling crash recovery via REDO logs"},
                    {"key": "B", "text": "By duplicating all tables into JSON files on every transaction"},
                    {"key": "C", "text": "By executing queries exclusively in RAM without disk commits"},
                    {"key": "D", "text": "By compressing SQL query strings using Brotli"}
                ],
                "correct_option": "A",
                "explanation": "WAL guarantees that changes are committed to sequential append-only log files before dirty buffer pool pages are flushed, allowing crash recovery to replay changes."
            }
        ]
    },
    "Computer Networks": {
        "Easy": [
            {
                "question_text": "Which OSI layer is responsible for end-to-end communication, flow control, and error recovery (e.g., TCP, UDP)?",
                "topic": "OSI Model vs TCP/IP Protocol Suite",
                "options": [
                    {"key": "A", "text": "Transport Layer (Layer 4)"},
                    {"key": "B", "text": "Network Layer (Layer 3)"},
                    {"key": "C", "text": "Data Link Layer (Layer 2)"},
                    {"key": "D", "text": "Physical Layer (Layer 1)"}
                ],
                "correct_option": "A",
                "explanation": "Layer 4 (Transport Layer) provides host-to-host communication services, flow control, and port addressing."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the primary functional difference between TCP and UDP?",
                "topic": "UDP vs TCP Protocol Characteristics",
                "options": [
                    {"key": "A", "text": "TCP is connection-oriented, reliable, and ordered; UDP is connectionless, lightweight, and unordered"},
                    {"key": "B", "text": "UDP guarantees packet delivery while TCP does not"},
                    {"key": "C", "text": "TCP only runs over optical fiber"},
                    {"key": "D", "text": "UDP encrypts all packets automatically"}
                ],
                "correct_option": "A",
                "explanation": "TCP provides ordered, reliable packet transmission via handshakes and acknowledgments. UDP trades reliability for low-latency transmission without acknowledgments."
            }
        ],
        "Medium": [
            {
                "question_text": "What are the three packets exchanged during a standard TCP connection handshake?",
                "topic": "TCP 3-Way Handshake, Flow Control & Congestion Control",
                "options": [
                    {"key": "A", "text": "SYN -> SYN-ACK -> ACK"},
                    {"key": "B", "text": "ACK -> SYN -> FIN"},
                    {"key": "C", "text": "HELLO -> READY -> CONNECT"},
                    {"key": "D", "text": "GET -> POST -> OK"}
                ],
                "correct_option": "A",
                "explanation": "The client initiates with SYN, the server responds with SYN-ACK, and the client confirms with ACK to establish a bidirectional stream."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In DNS architecture, what record type maps a domain name directly to an IPv6 address?",
                "topic": "DNS Resolution Architecture & Record Types",
                "options": [
                    {"key": "A", "text": "AAAA Record"},
                    {"key": "B", "text": "A Record"},
                    {"key": "C", "text": "CNAME Record"},
                    {"key": "D", "text": "MX Record"}
                ],
                "correct_option": "A",
                "explanation": "A records map hostnames to 32-bit IPv4 addresses; AAAA records map hostnames to 128-bit IPv6 addresses."
            }
        ],
        "Hard": [
            {
                "question_text": "How does HTTP/3 (QUIC) resolve head-of-line blocking that occurs at the transport layer in HTTP/2?",
                "topic": "HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)",
                "options": [
                    {"key": "A", "text": "It runs over UDP with independent streams; a lost packet on one stream does not pause other concurrent streams"},
                    {"key": "B", "text": "It forces clients to download the entire website in 1 TCP packet"},
                    {"key": "C", "text": "It disables TLS encryption completely"},
                    {"key": "D", "text": "It converts all HTTP requests to DNS queries"}
                ],
                "correct_option": "A",
                "explanation": "HTTP/2 multiplexes streams over a single TCP connection, so packet loss on one stream halts all streams. QUIC runs over UDP with stream multiplexing at the transport layer, eliminating TCP head-of-line blocking."
            }
        ]
    },
    "DevOps Engineer": {
        "Easy": [
            {
                "question_text": "What is the primary role of a `Dockerfile` in modern software development?",
                "topic": "Docker Containerization & Multi-stage Builds",
                "options": [
                    {"key": "A", "text": "A text script containing instructions to assemble and build a container image"},
                    {"key": "B", "text": "A database migration script"},
                    {"key": "C", "text": "A DNS record configuration file"},
                    {"key": "D", "text": "An SSL certificate generator"}
                ],
                "correct_option": "A",
                "explanation": "A Dockerfile defines the instructions (base image, dependencies, files, environment variables, commands) to build a container image."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the key advantage of Docker multi-stage builds when producing production container images?",
                "topic": "Docker Containerization & Multi-stage Builds",
                "options": [
                    {"key": "A", "text": "They separate build tools and intermediate artifacts from the final image, drastically reducing image size and attack surface"},
                    {"key": "B", "text": "They allow containers to run multiple operating systems simultaneously"},
                    {"key": "C", "text": "They bypass container registries and deploy directly to bare metal"},
                    {"key": "D", "text": "They disable all Linux cgroup boundaries for maximum performance"}
                ],
                "correct_option": "A",
                "explanation": "Multi-stage builds allow developers to compile code in heavy build stages and copy only compiled artifacts into a minimal production base image (e.g. Alpine)."
            }
        ],
        "Medium": [
            {
                "question_text": "In Kubernetes, which resource controller is typically used to guarantee that a copy of a Pod runs on every Node in the cluster?",
                "topic": "Kubernetes Pods, Deployments & DaemonSets",
                "options": [
                    {"key": "A", "text": "DaemonSet"},
                    {"key": "B", "text": "Deployment"},
                    {"key": "C", "text": "StatefulSet"},
                    {"key": "D", "text": "ReplicaSet"}
                ],
                "correct_option": "A",
                "explanation": "A DaemonSet ensures that all (or eligible) Nodes run a copy of a Pod, commonly utilized for log forwarders and node monitoring agents."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In Terraform, why is configuring remote state locking (e.g., via AWS DynamoDB) essential for engineering teams?",
                "topic": "Infrastructure as Code (Terraform & State Locking)",
                "options": [
                    {"key": "A", "text": "It prevents concurrent execution of `terraform apply` operations from corrupting the infrastructure state file"},
                    {"key": "B", "text": "It encrypts server passwords inside bash scripts"},
                    {"key": "C", "text": "It reduces cloud billing costs by caching EC2 instances"},
                    {"key": "D", "text": "It compiles HCL configuration files into C++ binaries"}
                ],
                "correct_option": "A",
                "explanation": "Remote state locking ensures that only one team member or CI pipeline can execute operations mutating the state file at any moment, avoiding race conditions."
            }
        ],
        "Hard": [
            {
                "question_text": "How does a Canary deployment differ from a Blue-Green deployment when rolling out new microservices?",
                "topic": "Zero-Downtime Deployments (Blue-Green & Canary)",
                "options": [
                    {"key": "A", "text": "Canary routes a small percentage of real production traffic (e.g., 5%) to the new release to monitor metrics before full rollout; Blue-Green cuts over 100% of traffic once verified"},
                    {"key": "B", "text": "Canary deployments require stopping all production databases during rollout"},
                    {"key": "C", "text": "Blue-Green deployments can only be deployed on bare metal servers"},
                    {"key": "D", "text": "Canary deployments do not support rollback"}
                ],
                "correct_option": "A",
                "explanation": "Canary gradually routes a sliver of traffic to the new version while monitoring error rates and latency, limiting blast radius. Blue-Green switches 100% of traffic between two identical production environments."
            }
        ]
    }
}

# Structure: ROLE -> DIFFICULTY -> List of questions
FALLBACK_TEXT_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Python Developer": {
        "Easy": [
            {
                "question_text": "Explain the difference between mutable and immutable data types in Python. Give two examples of each, and explain what happens when you attempt to modify an immutable object.",
                "topic": "Python Data Types & Collections",
                "model_answer": "In Python, mutable objects can have their state or contents changed in-place without altering their memory identity (id()), whereas immutable objects cannot be modified once instantiated.\n\n- **Mutable examples**: list, dict, set.\n- **Immutable examples**: int, float, str, tuple, frozenset.\n\nWhen attempting to modify an immutable object (e.g., modifying a tuple index or concatenating a string), Python either raises a TypeError (for reassignment) or constructs an entirely new object in memory and updates the reference."
            },
            {
                "question_text": "How does Python handle argument passing to functions? Explain the concept of 'pass-by-object-reference' and how it impacts mutable versus immutable arguments.",
                "topic": "Functions & Variable Scope",
                "model_answer": "Python uses pass-by-object-reference (or call-by-sharing). When you pass a variable to a function, the function receives a copy of the reference pointing to the existing object.\n\n- **Immutable objects** (int, str, tuple): Rebinding the parameter inside the function assigns the local name to a new object without mutating the caller's variable.\n- **Mutable objects** (list, dict): In-place modifications (e.g. `lst.append()`) alter the shared object in memory, visibly affecting the caller's reference."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is a Python decorator, and how does it work behind the scenes? Provide a concise code example demonstrating a timer or logging decorator.",
                "topic": "Decorators & Generators",
                "model_answer": "A decorator in Python is a callable that accepts another function as an argument, extends or alters its behavior without modifying its source code, and returns a callable.\n\nBehind the scenes, the `@decorator` syntax is syntactic sugar for `target_func = decorator(target_func)`.\n\nExample:\n```python\nimport functools\n\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n```"
            },
            {
                "question_text": "Explain the lifecycle and execution sequence of a Python `try...except...else...finally` statement. When would you use the `else` block?",
                "topic": "Error Handling & Debugging",
                "model_answer": "1. **try**: The code under observation runs.\n2. **except**: Executes if an exception matching the exception type is raised in the `try` block.\n3. **else**: Executes if and only if the `try` block finishes successfully without raising any exceptions. It prevents accidental catching of exceptions raised by subsequent processing code.\n4. **finally**: Always executes regardless of whether an exception occurred, was handled, or a return statement was encountered, making it ideal for resource cleanup (e.g., closing file descriptors or database connections)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain how generator functions and the `yield` statement enable memory-efficient data processing in Python. Contrast this with loading large datasets into lists.",
                "topic": "Decorators & Generators",
                "model_answer": "A standard function computes all results eagerly and returns them as a populated list, requiring O(N) memory proportional to dataset size. When processing multi-gigabyte logs or database streams, this causes memory exhaustion.\n\nGenerator functions use `yield` to return an iterator. When called, execution pauses at `yield`, retaining local scope state. Values are produced lazily on demand (O(1) memory), allowing streams of arbitrary size to be piped through generators efficiently."
            },
            {
                "question_text": "What is the difference between shallow copy (`copy.copy`) and deep copy (`copy.deepcopy`) in Python? Explain with a scenario involving nested collections.",
                "topic": "Memory Management & Reference Counting",
                "model_answer": "- **Shallow Copy (`copy.copy`)**: Constructs a new collection object, but populates it with references to the child objects contained in the original. If a nested list or dictionary inside the shallow copy is mutated, the change is reflected in the original collection.\n- **Deep Copy (`copy.deepcopy`)**: Recursively constructs new copies of both the parent container and all nested child objects. Mutating elements within the copy leaves the original completely unmodified."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Discuss Python's Global Interpreter Lock (GIL). What problem does it solve, how does it impact multi-threaded CPU-bound versus I/O-bound programs, and how do you achieve parallelism for CPU-heavy tasks?",
                "topic": "GIL & Multithreading vs Multiprocessing",
                "model_answer": "The CPython GIL is a mutual-exclusion lock that prevents multiple native threads from executing Python bytecodes simultaneously. It was designed to safeguard CPython's reference-counting memory management from race conditions.\n\n- **I/O-Bound Tasks**: Multithreading works well because threads voluntarily release the GIL while waiting on network or disk I/O.\n- **CPU-Bound Tasks**: Multithreading degrades performance due to lock contention overhead across cores.\n- **Parallelism Solution**: Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` to spawn separate OS processes with isolated memory spaces and distinct GILs."
            },
            {
                "question_text": "Explain how asynchronous I/O with Python's `asyncio` works under the hood. Contrast coroutines running on an event loop with traditional multi-threaded concurrency.",
                "topic": "Asynchronous Programming (asyncio)",
                "model_answer": "`asyncio` provides single-threaded, cooperative multitasking based on an event loop. Coroutines (`async def`) pause execution when encountering an `await` on an I/O operation (socket read, timer), yielding execution back to the event loop. The loop polls OS primitives (epoll/kqueue) and resumes the coroutine when the I/O event is ready.\n\nUnlike multi-threading, which involves preemptive OS context switches, lock synchronization, and thread stack overhead (typically ~8MB per thread), asyncio tasks are lightweight Python objects with minimal memory footprint and zero race conditions during synchronous execution blocks."
            }
        ],
        "Hard": [
            {
                "question_text": "Explain Python's two-tiered memory management system involving reference counting and the cyclic generational garbage collector. Describe how circular references are detected and how developers should profile memory leaks in production.",
                "topic": "Memory Management & Reference Counting",
                "model_answer": "CPython uses a two-tiered memory architecture:\n1. **Reference Counting**: Every PyObject has an `ob_refcnt` counter. When references are assigned, it increments; when deleted or out of scope, it decrements. When it hits 0, memory is immediately reclaimed.\n2. **Generational Cyclic GC**: Reference counting cannot reclaim circular graphs (A references B, B references A). Python has a cyclic garbage collector organized into Generations 0, 1, and 2. It periodically detects isolated graphs using a pointer traversal algorithm.\n\nIn production, developers profile memory leaks using `tracemalloc`, `gc.collect()`, `objgraph`, and `weakref` proxies to prevent circular leaks."
            },
            {
                "question_text": "Explain the Python Descriptor protocol (`__get__`, `__set__`, `__delete__`). Describe how descriptors power Python features such as `@property`, methods, and `@classmethod`, and when you would implement a custom descriptor.",
                "topic": "Object-Oriented Python",
                "model_answer": "A descriptor is any object that defines at least one of `__get__()`, `__set__()`, or `__delete__()`. In Python, attribute access on an instance (`instance.attr`) triggers `Class.__dict__['attr'].__get__(instance, Class)` if `attr` is a descriptor.\n\n- **Properties**: `@property` implements a descriptor returning calculated values.\n- **Methods**: Functions define `__get__`, which binds the function to `instance` when accessed as an attribute, creating a bound method.\n- **Use Cases**: Custom descriptors are used for declarative ORM field validation (like SQLAlchemy or Django model fields), lazy caching attributes, and framework typing enforcement."
            }
        ]
    },
    "Java Developer": {
        "Easy": [
            {
                "question_text": "Explain the four core principles of Object-Oriented Programming (Encapsulation, Inheritance, Polymorphism, Abstraction) and how they are implemented in Java.",
                "topic": "Core Java OOP & Polymorphism",
                "model_answer": "1. **Encapsulation**: Bundling fields and methods within classes while restricting direct field access via private access modifiers and public getters/setters.\n2. **Inheritance**: Deriving classes from base classes using `extends`, promoting code reuse.\n3. **Polymorphism**: The ability of an object to take on many forms, implemented via method overloading (compile-time) and method overriding (runtime).\n4. **Abstraction**: Hiding implementation details and showing only essential interfaces via abstract classes and interfaces."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the difference between Checked and Unchecked exceptions in Java. When should you design a custom exception as checked versus unchecked?",
                "topic": "Core Java OOP & Polymorphism",
                "model_answer": "- **Checked Exceptions**: Subclasses of `Exception` (excluding `RuntimeException`). The compiler forces callers to handle them via try-catch or declare them with `throws`. Used for recoverable scenarios (e.g., FileNotFoundException, SQLException).\n- **Unchecked Exceptions**: Subclasses of `RuntimeException` and `Error`. Handled optionally at runtime, typically representing programming logic flaws (e.g., NullPointerException, IllegalArgumentException).\n\nModern Java best practice favors unchecked exceptions for business domain logic, avoiding boilerplate `throws` declarations."
            }
        ],
        "Medium": [
            {
                "question_text": "Describe the internal architecture and collision resolution mechanism of Java's `HashMap`. How did this change between Java 7 and Java 8?",
                "topic": "Java Collections Framework & Internals",
                "model_answer": "Java's HashMap uses an array of buckets (`Node<K,V>[]`). The key's hashCode is spread across buckets using bitwise hashing `(n - 1) & hash`.\n\n- **In Java 7**: Collisions were chained using singly linked lists. In worst-case collisions, lookup degraded to O(N).\n- **In Java 8**: When a bucket's linked list reaches `TREEIFY_THRESHOLD` (8) and the array has at least 64 buckets, it converts the list into a balanced Red-Black Tree (`TreeNode`). This optimizes worst-case search, insertion, and deletion times from O(N) to O(log N)."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain the Java Memory Model (JMM), the happens-before relationship, and the role of the `volatile` keyword in thread safety.",
                "topic": "Java Concurrency & Multi-threading",
                "model_answer": "The JMM defines how threads interact through shared memory and how local CPU caches synchronize with main memory.\n\n- **Happens-Before**: Guarantees that memory writes by one thread are visible to reads by another thread without instruction reordering.\n- **`volatile`**: Ensures direct memory visibility and prevents compiler instruction reordering. Any write to a volatile variable happens-before subsequent reads of that variable. However, volatile does not guarantee compound atomicity (e.g. `count++`), which requires `AtomicInteger` or `synchronized`."
            }
        ],
        "Hard": [
            {
                "question_text": "Explain how Dependency Injection works in Spring Boot and discuss how Spring manages Bean lifecycles and scopes (Singleton vs Prototype).",
                "topic": "Spring Boot & Dependency Injection",
                "model_answer": "Spring's IoC (Inversion of Control) container manages component creation, configuration, and lifecycle via Dependency Injection (constructor, setter, or field injection).\n\n- **Singleton Scope (Default)**: Exactly one shared bean instance per ApplicationContext, instantiated on startup, suitable for stateless services.\n- **Prototype Scope**: A brand new instance is created every time the bean is requested from the container.\n\nLifecycle callbacks (`@PostConstruct`, `InitializingBean`, `@PreDestroy`) allow initialization and clean teardown of resources."
            }
        ]
    },
    "Frontend Developer": {
        "Easy": [
            {
                "question_text": "Explain the difference between `let`, `const`, and `var` in modern JavaScript with respect to scoping and hoisting.",
                "topic": "JavaScript ES6+ & DOM Manipulation",
                "model_answer": "- **`var`**: Function-scoped (or global), hoisted to the top of its scope initialized as `undefined`, and permits redeclaration.\n- **`let`**: Block-scoped (enclosed within `{}`), hoisted into a Temporal Dead Zone (TDZ) where accessing before declaration throws a ReferenceError, and permits reassignment but not redeclaration.\n- **`const`**: Block-scoped, hoisted in TDZ, and cannot be reassigned (though internal properties of objects/arrays assigned to const remain mutable)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the Virtual DOM in React, how does the reconciliation algorithm operate, and why are keys essential in lists?",
                "topic": "React Hooks & Component Lifecycle",
                "model_answer": "The Virtual DOM is an in-memory lightweight representation of the real DOM. When state changes, React constructs a new VDOM tree and diffs it against the previous snapshot using an O(N) heuristic reconciliation algorithm.\n\nKeys provide stable identity across renders. Without keys, React compares children by index, resulting in unnecessary DOM recreations and corrupted form input state. Providing unique keys lets React determine insertions, moves, and deletions with minimal real DOM mutations."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain the Critical Rendering Path (CRP) in web browsers. Detail the sequence from HTML parsing to pixel paint and how CSS/JavaScript can block rendering.",
                "topic": "Critical Rendering Path & Bundle Splitting",
                "model_answer": "The CRP sequence:\n1. **DOM Tree**: HTML parser converts bytes -> tokens -> nodes -> DOM tree.\n2. **CSSOM Tree**: CSS is parsed into the CSS Object Model (render-blocking by default).\n3. **Render Tree**: DOM + CSSOM combine to compute visible elements.\n4. **Layout (Reflow)**: Computes geometry and exact coordinates of each element.\n5. **Painting**: Fills pixels on screen (rasterization).\n6. **Compositing**: GPU combines painted layers.\n\nSynchronous `<script>` tags pause HTML parsing because scripts can mutate DOM. Using `<script defer>` or `<script async>` prevents parser blocking."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Detail strategies for optimizing Core Web Vitals, specifically targeting Largest Contentful Paint (LCP) and Interaction to Next Paint (INP).",
                "topic": "Core Web Vitals & Web Performance",
                "model_answer": "- **LCP Optimization**: Preload hero images using `<link rel=\"preload\">`, deliver responsive modern image formats (AVIF/WebP), deploy edge CDN caching, and inline critical CSS.\n- **INP Optimization**: Break up long main-thread tasks (>50ms) using `requestIdleCallback` or `setTimeout(0)`, code-split heavy JavaScript bundles via dynamic `import()`, debounce/throttle expensive calculations, and delegate CPU-heavy parsing to Web Workers."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a resilient client-side state management architecture for a high-traffic web application. Compare normalized stores versus local component state, and discuss cache invalidation.",
                "topic": "State Management Architecture (Redux/Zustand)",
                "model_answer": "A scalable state architecture segregates state into three tiers:\n1. **Server Cache State** (via React Query/SWR): Normalized caching, automatic background revalidation (stale-while-revalidate), and optimistic UI updates.\n2. **Global Client State** (via Zustand/Redux): Normalized entity dictionaries (keyed by ID) to prevent duplication and enable O(1) lookups.\n3. **Local Component State** (via useState/useReducer): Ephemeral UI concerns (dropdown toggles, input focus).\n\nImmutability is enforced so components rely on shallow reference equality checks (`prev !== next`) to avoid unnecessary re-renders."
            }
        ]
    },
    "Backend Developer": {
        "Easy": [
            {
                "question_text": "What are the core characteristics of a RESTful API? Explain the standard HTTP methods (GET, POST, PUT, DELETE, PATCH) and their intended purposes.",
                "topic": "REST API Design & Idempotency",
                "model_answer": "REST (Representational State Transfer) is a stateless, client-server architectural style using standard HTTP verbs and URI resource paths:\n- **GET**: Safely retrieves resource representations without modifying server state.\n- **POST**: Creates a new resource under the specified collection.\n- **PUT**: Replaces the target resource completely (idempotent).\n- **PATCH**: Partially updates fields of a target resource.\n- **DELETE**: Removes the specified resource (idempotent)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain database indexing with B-Trees. How does an index accelerate SELECT queries, and what are the trade-offs on INSERT and UPDATE operations?",
                "topic": "Database Indexing (B-Tree, Hash, GIN) & Query Plans",
                "model_answer": "A B-Tree index is a balanced, multi-way search tree that keeps keys sorted and allows search, sequential access, insertions, and deletions in O(log N) time.\n- **Acceleration**: Instead of scanning millions of disk blocks sequentially (Seq Scan), the database traverses root -> branch -> leaf pages to pinpoint matching row pointers.\n- **Trade-offs**: Every index consumes additional disk space, and every INSERT, UPDATE, or DELETE must update the B-Tree index structures, adding write latency."
            }
        ],
        "Medium": [
            {
                "question_text": "Describe the trade-offs between SQL (Relational) and NoSQL databases. When would you choose PostgreSQL versus MongoDB or Cassandra for a high-throughput production service?",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "model_answer": "- **Relational (PostgreSQL)**: Strong ACID guarantees, strict schemas, and complex relational querying via JOINs. Best for financial ledgers, inventory, and relational domains where data integrity is paramount.\n- **Document NoSQL (MongoDB)**: Flexible, schema-less JSON documents with horizontal sharding. Best for rapidly evolving data shapes and hierarchical content.\n- **Wide-Column NoSQL (Cassandra)**: Masterless peer-to-peer clustering with tunable eventual consistency. Best for high-write time-series, analytics telemetry, and massive horizontal scale."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "How do you securely implement JWT-based authentication in a distributed microservices environment while handling token revocation and refresh token rotation?",
                "topic": "Authentication, JWT Security & Refresh Rotation",
                "model_answer": "1. **Token Hierarchy**: Issue short-lived access tokens (15 mins) and long-lived refresh tokens (7 days) stored in HttpOnly, Secure, SameSite cookies to protect against XSS and CSRF.\n2. **Refresh Token Rotation**: Each time a refresh token is used, it is invalidated and replaced with a newly generated pair. If an already-used refresh token is presented, token theft is detected, and the entire token family is immediately revoked.\n3. **Revocation**: Stateless JWT access tokens can be revoked before expiry by maintaining a lightweight distributed denylist (keyed by JWT JTI ID) in Redis with automatic TTL expiration."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a high-throughput, fault-tolerant rate-limiting system for an API gateway handling millions of requests per second. Compare Token Bucket, Leaky Bucket, and Sliding Window Counter algorithms.",
                "topic": "API Rate Limiting & Token Bucket Algorithms",
                "model_answer": "1. **Algorithms**:\n   - **Token Bucket**: Allows bursts up to bucket capacity while enforcing an average refill rate.\n   - **Leaky Bucket**: Smooths traffic into a constant output rate, discarding excess overflow.\n   - **Sliding Window Counter**: Balances exact window accuracy with minimal memory by combining previous and current window counts with a weighted ratio.\n2. **Distributed Architecture**: Use Redis with atomic Lua scripts to execute check-and-decrement in a single round-trip without race conditions. Deploy local in-memory token buffers at the gateway to reduce Redis network hops."
            }
        ]
    },
    "Data Analyst": {
        "Easy": [
            {
                "question_text": "What is the difference between an INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL? Provide simple examples of the resulting datasets.",
                "topic": "SQL Window Functions & Aggregations",
                "model_answer": "- **INNER JOIN**: Returns only rows where there is a match in both tables.\n- **LEFT JOIN**: Returns all rows from the left table and matching rows from the right table. Non-matching right columns are filled with NULL.\n- **FULL OUTER JOIN**: Returns all rows from both tables, filling with NULL wherever there is no match on either side."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain common techniques for identifying and treating missing values in a tabular analytical dataset. When is imputation appropriate versus deletion?",
                "topic": "Data Cleaning & Missing Value Imputation",
                "model_answer": "- **Missingness Mechanisms**: MCAR (Completely at Random), MAR (At Random), MNAR (Not at Random).\n- **Deletion**: Listwise deletion is safe only if MCAR and missingness is tiny (<5%), otherwise it introduces sample bias and data loss.\n- **Imputation**: Mean/median imputation preserves sample size for numerical data; mode for categorical data. For time-series, forward-fill (LOCF) or linear interpolation is standard. Advanced methods use KNN or MICE regression."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain SQL Window Functions and compare `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`. Provide a scenario demonstrating where each is used.",
                "topic": "SQL Window Functions & Aggregations",
                "model_answer": "Window functions compute calculations across a set of table rows related to the current row without collapsing rows like `GROUP BY`.\n- **`ROW_NUMBER()`**: Strictly consecutive integers (1, 2, 3, 4) with no ties.\n- **`RANK()`**: Assigns duplicate ranks to ties and skips subsequent ranks (1, 2, 2, 4).\n- **`DENSE_RANK()`**: Assigns duplicate ranks to ties without skipping subsequent ranks (1, 2, 2, 3).\n\nUse `ROW_NUMBER()` for pagination or deduplication; use `DENSE_RANK()` for top-N ranking (e.g. top 3 salaries)."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain the statistical methodology of A/B testing. Detail sample size determination, statistical significance, p-values, Type I and Type II errors.",
                "topic": "A/B Testing, Hypothesis Testing & P-Values",
                "model_answer": "A/B testing evaluates variants against a control:\n1. **Hypothesis**: Null H0 (no difference) vs Alternative H1 (variant changes metric).\n2. **Type I Error (Alpha, 5%)**: False positive; rejecting H0 when it was true.\n3. **Type II Error (Beta, 20%)**: False negative; failing to reject H0 when an effect existed (Statistical Power = 1 - Beta = 80%).\n4. **Sample Size**: Calculated upfront based on baseline conversion, Minimum Detectable Effect (MDE), alpha, and beta.\n5. **P-Value**: The probability of observing results at least as extreme as the experiment under H0. If p < alpha, reject H0."
            }
        ],
        "Hard": [
            {
                "question_text": "Compare Star Schema and Snowflake Schema in enterprise data warehousing. Discuss query performance, ETL complexity, and analytical storage trade-offs.",
                "topic": "Star Schema vs Snowflake Data Modeling",
                "model_answer": "- **Star Schema**: Denormalized dimension tables directly linked to central fact tables. Query execution is fast with minimal JOINs, ideal for OLAP column-oriented stores (BigQuery, Snowflake), though storage has minor redundancy.\n- **Snowflake Schema**: Normalized dimension tables with sub-dimension hierarchies (e.g., product -> subcategory -> category). Eliminates redundancy but adds multiple JOIN operations, increasing query latency and analytical query complexity."
            }
        ]
    },
    "Machine Learning Engineer": {
        "Easy": [
            {
                "question_text": "Explain the fundamental difference between Supervised Learning, Unsupervised Learning, and Reinforcement Learning, giving one real-world application for each.",
                "topic": "Supervised vs Unsupervised Learning Algorithms",
                "model_answer": "- **Supervised Learning**: Models learn from labeled training pairs (input X, ground truth Y). Application: Email spam detection or loan default prediction.\n- **Unsupervised Learning**: Models identify hidden patterns or clusters in unlabeled data without target labels. Application: Customer segmentation (K-Means) or anomaly detection.\n- **Reinforcement Learning**: Agents learn optimal policies by interacting with an environment through trial-and-error, maximizing cumulative scalar rewards. Application: Autonomous driving navigation or game playing (AlphaGo)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the Bias-Variance tradeoff in machine learning. How do model complexity, overfitting, and underfitting relate to this tradeoff?",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "model_answer": "- **Bias**: Error from erroneous assumptions in the learning algorithm (underfitting). High bias models (e.g., linear regression on non-linear data) fail to capture underlying patterns.\n- **Variance**: Error from sensitivity to small fluctuations in training data (overfitting). High variance models (e.g., deep unpruned decision trees) memorize noise, failing on test sets.\n- **Tradeoff**: Total error = Bias^2 + Variance + Irreducible Error. Optimal models minimize total error by balancing complexity via regularization, cross-validation, and pruning."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain precision, recall, F1-score, and ROC-AUC. Why is accuracy an unreliable metric on severely imbalanced datasets?",
                "topic": "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
                "model_answer": "Accuracy is `(TP + TN) / Total`. On imbalanced datasets (e.g. 99% negative fraud cases), a naive model predicting 100% negative achieves 99% accuracy while catching zero fraud.\n- **Precision**: `TP / (TP + FP)` - When the model predicts positive, how often is it right?\n- **Recall (Sensitivity)**: `TP / (TP + FN)` - What fraction of actual positives did the model capture?\n- **F1-Score**: Harmonic mean of precision and recall `2 * (P * R) / (P + R)`.\n- **ROC-AUC**: Measures classification capability across all decision thresholds by plotting True Positive Rate vs False Positive Rate."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Describe methods for handling severe class imbalance in tabular datasets, including resampling strategies (SMOTE, undersampling) and algorithmic approaches (cost-sensitive learning, focal loss).",
                "topic": "Handling Class Imbalance (SMOTE, Focal Loss)",
                "model_answer": "1. **Resampling**:\n   - **SMOTE (Synthetic Minority Over-sampling)**: Synthesizes new minority examples along line segments connecting k-nearest neighbors in feature space.\n   - **Random Undersampling**: Reduces majority instances, but risks discarding valuable data.\n2. **Algorithmic Solutions**:\n   - **Class Weighting / Cost-Sensitive**: Penalizes misclassifications of minority samples higher in loss function (e.g., `class_weight='balanced'`).\n   - **Focal Loss**: Dynamically down-weights easy examples, focusing gradient updates on hard-to-classify samples.\n3. **Threshold Tuning**: Adjusting decision thresholds away from default 0.5 to optimize F1 or Recall."
            }
        ],
        "Hard": [
            {
                "question_text": "Detail how you would detect and remediate Data Drift and Concept Drift in a production machine learning service. Outline monitoring architectures and retraining pipelines.",
                "topic": "Data Drift, Concept Drift & Model Monitoring",
                "model_answer": "1. **Definitions**:\n   - **Data (Covariate) Drift**: Feature distribution P(X) changes over time while relationship P(Y|X) remains constant.\n   - **Concept Drift**: Underlying statistical relationship P(Y|X) changes (e.g., consumer behavior shifts post-pandemic).\n2. **Detection**:\n   - Statistical distance tests (Kolmogorov-Smirnov test for numerical features, Population Stability Index (PSI), Wasserstein distance).\n3. **Architecture**:\n   - Real-time telemetry logging of inference inputs and ground-truth arrival.\n   - Automated threshold triggers in monitoring (Evidently/Whylogs) that trigger automated validation and retraining pipelines."
            }
        ]
    },
    "Database Administrator": {
        "Easy": [
            {
                "question_text": "Explain the ACID properties of relational database transactions and provide a short example of why each property is critical.",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "model_answer": "- **Atomicity**: Transactions are all-or-nothing units. If a transfer deducts $100 from Account A, Account B must receive $100 or the entire transaction rolls back.\n- **Consistency**: Database state transitions from one valid state to another, satisfying all schema constraints, checks, and foreign keys.\n- **Isolation**: Concurrent transactions execute without interfering with one another.\n- **Durability**: Once committed, changes survive server crashes or power failures via persistent write-ahead logs."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the difference between First, Second, and Third Normal Form (1NF, 2NF, 3NF). Why do databases normalize schemas?",
                "topic": "Relational Schema Design & 3NF Normalization",
                "model_answer": "- **1NF**: Atomic column values with no repeating groups.\n- **2NF**: Meets 1NF, and all non-key attributes are fully functionally dependent on the entire primary key (eliminates partial key dependencies).\n- **3NF**: Meets 2NF, and no non-key attribute is transitively dependent on another non-key attribute.\n\nNormalization eliminates duplicate storage and protects against anomalies during insert, update, and delete operations."
            }
        ],
        "Medium": [
            {
                "question_text": "How do B-Tree indexes work in relational database engines? Discuss composite index column ordering and index selectivity.",
                "topic": "B-Tree vs Hash vs Bitmap Index Architecture",
                "model_answer": "A B-Tree is a balanced search tree where leaf nodes contain indexed values and direct tuple pointers (TID/RowID).\n- **Composite Index Ordering**: An index on `(col_a, col_b)` can satisfy queries filtering on `col_a` alone or `col_a AND col_b`, but CANNOT satisfy queries filtering solely on `col_b` (leftmost prefix rule).\n- **Selectivity**: Highly selective columns (unique values) provide optimal index efficiency; low-cardinality columns (e.g. boolean flags) often cause the query planner to prefer sequential scans."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain database deadlocks. How do database engines detect them, and what architectural strategies prevent deadlocks in high-concurrency systems?",
                "topic": "Locking Mechanisms & Deadlock Resolution",
                "model_answer": "A deadlock occurs when two transactions hold locks that the other requires (Transaction 1 locks row A and waits for B; Transaction 2 locks row B and waits for A).\n- **Detection**: Engines use wait-for graph cycle detection. When a directed cycle is found, the engine aborts and rolls back the transaction with the lowest cost.\n- **Prevention**:\n  1. Always acquire locks in a globally consistent order across all transactions.\n  2. Keep transactions short and avoid user interactive pauses within open transactions.\n  3. Use optimistic locking (version columns) rather than pessimistic SELECT FOR UPDATE."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a high-availability and disaster recovery architecture for an enterprise PostgreSQL database. Compare streaming replication, connection pooling, and automated failover.",
                "topic": "Database Replication (Synchronous vs Asynchronous)",
                "model_answer": "1. **Replication**: Primary node streaming WAL records to multiple standby replicas. Synchronous replication for zero data loss (RPO=0) on primary standby; asynchronous replication for read-scaling replicas.\n2. **Connection Pooling**: Deploy PgBouncer in transaction pooling mode to handle thousands of client connections without exceeding backend PostgreSQL memory limits.\n3. **Failover**: Use Patroni with distributed consensus (etcd/Consul) to manage leader elections, ensuring automated promotion without split-brain scenarios.\n4. **Backup**: Continuous WAL archiving to S3 with pgBackRest for Point-In-Time Recovery (PITR)."
            }
        ]
    },
    "Computer Networks": {
        "Easy": [
            {
                "question_text": "Explain the 7 layers of the OSI model and describe the primary function of each layer.",
                "topic": "OSI Model vs TCP/IP Protocol Suite",
                "model_answer": "1. **Physical (L1)**: Raw bit transmission over physical media (cables, radio).\n2. **Data Link (L2)**: Node-to-node frame delivery, MAC addressing, error detection.\n3. **Network (L3)**: Packet routing across networks, logical IP addressing.\n4. **Transport (L4)**: End-to-end communication, segmentation, flow control (TCP/UDP).\n5. **Session (L5)**: Establishes, manages, and terminates session dialogues.\n6. **Presentation (L6)**: Data formatting, serialization, encryption/decryption (TLS).\n7. **Application (L7)**: End-user network services and protocols (HTTP, DNS, SSH)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the complete step-by-step process of DNS resolution when a user types a URL (e.g. https://example.com) into a web browser.",
                "topic": "DNS Resolution Architecture & Record Types",
                "model_answer": "1. Browser checks local cache -> OS checks hosts file & resolver cache.\n2. Request forwarded to Recursive DNS Resolver (ISP or 8.8.8.8).\n3. Resolver queries Root Nameserver (.), which refers to `.com` TLD Nameserver.\n4. Resolver queries `.com` TLD Nameserver, which refers to Authoritative Nameserver for `example.com`.\n5. Resolver queries Authoritative Nameserver, which returns the A/AAAA IP address.\n6. Resolver caches IP with TTL and returns it to the client browser."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain the TCP 3-way handshake and 4-way termination process. Detail the flags (SYN, ACK, FIN) and why TIME_WAIT state exists.",
                "topic": "TCP 3-Way Handshake, Flow Control & Congestion Control",
                "model_answer": "- **3-Way Handshake**: Client sends SYN(seq=x) -> Server replies SYN(seq=y), ACK(x+1) -> Client sends ACK(y+1). Both sides synchronize sequence numbers.\n- **4-Way Teardown**: Active closer sends FIN -> Passive side replies ACK (half-closed) -> Passive side sends FIN -> Active closer replies ACK.\n- **TIME_WAIT State**: The active closer waits for 2 * MSL (Maximum Segment Lifetime) to ensure the final ACK reached the peer and that delayed stray packets expire before the port is reused."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain the TLS 1.3 handshake sequence. How does it improve latency and security compared to TLS 1.2?",
                "topic": "TLS/SSL Handshake & Symmetric/Asymmetric Encryption",
                "model_answer": "- **Latency**: TLS 1.2 required 2 round-trip times (2-RTT) before application data could be sent. TLS 1.3 reduces the full handshake to 1-RTT (and supports 0-RTT resumption for returning clients) by combining key exchange with initial ClientHello.\n- **Security**: TLS 1.3 dropped legacy vulnerable algorithms (RSA key exchange, CBC ciphers, RC4, MD5, SHA-1). It enforces Forward Secrecy exclusively via Ephemeral Diffie-Hellman (ECDHE)."
            }
        ],
        "Hard": [
            {
                "question_text": "Explain TCP Congestion Control algorithms (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery) and contrast loss-based versus delay-based congestion control.",
                "topic": "TCP 3-Way Handshake, Flow Control & Congestion Control",
                "model_answer": "1. **Slow Start**: Congestion Window (cwnd) doubles every RTT until hitting `ssthresh`.\n2. **Congestion Avoidance**: cwnd increases linearly by 1 MSS per RTT.\n3. **Fast Retransmit**: Upon receiving 3 duplicate ACKs, retransmits the missing segment immediately without waiting for RTO timeout.\n4. **Fast Recovery**: Halves `ssthresh` and continues linear window growth without dropping back to cwnd=1.\n5. **Loss vs Delay-Based**: Loss-based (Reno, Cubic) fills buffer until packet drops occur; delay-based (BBR, Vegas) monitors RTT inflation to detect queue buildup before packet loss occurs."
            }
        ]
    },
    "DevOps Engineer": {
        "Easy": [
            {
                "question_text": "Explain the difference between a Virtual Machine (VM) and a Docker Container in terms of architecture, resource usage, and boot time.",
                "topic": "Docker Containerization & Multi-stage Builds",
                "model_answer": "- **Virtual Machines**: Run on a hypervisor (Type 1 or 2). Each VM contains a full guest operating system, virtualized hardware, and device drivers, resulting in gigabytes of storage and minute-long boot times.\n- **Docker Containers**: Share the host OS kernel and isolate processes using Linux kernel namespaces (PID, NET, MNT) and cgroups for resource quotas. Containers are lightweight (megabytes) and start in milliseconds."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is Infrastructure as Code (IaC)? Compare declarative (Terraform, CloudFormation) versus imperative (Ansible, bash scripts) approaches.",
                "topic": "Infrastructure as Code (Terraform & State Locking)",
                "model_answer": "IaC manages compute, networking, and storage through version-controlled configuration files rather than manual dashboard clicks.\n- **Declarative (Terraform)**: You declare the *desired end state*. The engine calculates the delta between current state and desired state, handling creation, modification, or deletion automatically.\n- **Imperative (Ansible/Scripts)**: You specify the exact sequence of steps to execute. It requires conditional logic to guarantee idempotency."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain Kubernetes core primitives: Pod, Deployment, Service (ClusterIP, NodePort, LoadBalancer), and Ingress Controller.",
                "topic": "Kubernetes Pods, Deployments & DaemonSets",
                "model_answer": "- **Pod**: Smallest deployable unit, encapsulating one or more co-located containers sharing network namespaces and storage volumes.\n- **Deployment**: Manages declarative replica sets, automated rolling updates, and rollbacks for stateless pods.\n- **ClusterIP**: Exposes service on internal cluster IP, accessible only within the cluster.\n- **NodePort**: Exposes service on a static port (30000-32767) on each node's IP.\n- **LoadBalancer**: Provisions a cloud provider external load balancer routing traffic to NodePorts.\n- **Ingress Controller**: Layer 7 reverse proxy managing HTTP/S routing, SSL termination, and host/path routing."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Describe the implementation of zero-downtime Blue-Green and Canary deployment pipelines using CI/CD and Kubernetes.",
                "topic": "Zero-Downtime Deployments (Blue-Green & Canary)",
                "model_answer": "- **Blue-Green**: Run two identical production environments (Blue = active, Green = idle). Deploy the new release to Green, run automated smoke tests, and switch router/service traffic instantaneously to Green. If anomalies occur, cut back to Blue.\n- **Canary (Argo Rollouts)**: Deploy new version receiving 5% traffic. Automated analysis monitors metrics (error rate, latency) for 15 minutes. If healthy, increase to 25%, 50%, 100%; if error rate spikes, immediately abort rollout."
            }
        ],
        "Hard": [
            {
                "question_text": "Design an enterprise observability architecture for a distributed microservices platform using Prometheus, Grafana, OpenTelemetry, and Jaeger.",
                "topic": "Observability & Monitoring (Prometheus & Grafana)",
                "model_answer": "1. **Three Pillars**:\n   - **Metrics (Prometheus)**: Numerical time-series metrics scraped periodically via pull model from `/metrics` endpoints. Displayed on Grafana dashboards and monitored via Alertmanager.\n   - **Logs (Fluentbit -> Loki)**: Structured JSON application logs aggregated with metadata tags.\n   - **Traces (OpenTelemetry + Jaeger)**: Distributed trace context propagation across microservices using W3C Trace Context headers, tracking end-to-end request latency across services.\n2. **High Availability**: Deploy Thanos or Cortex for long-term federated metric storage across clusters."
            }
        ]
    }
}

# Merge high-capacity multi-role expanded question banks
try:
    from app.services.expanded_question_banks import EXTRA_MCQ_BANK, EXTRA_TEXT_BANK
    for r_name, d_map in EXTRA_MCQ_BANK.items():
        if r_name in FALLBACK_MCQ_BANK:
            for d_level, q_items in d_map.items():
                FALLBACK_MCQ_BANK[r_name].setdefault(d_level, []).extend(q_items)
        else:
            FALLBACK_MCQ_BANK[r_name] = d_map

    for r_name, d_map in EXTRA_TEXT_BANK.items():
        if r_name in FALLBACK_TEXT_BANK:
            for d_level, q_items in d_map.items():
                FALLBACK_TEXT_BANK[r_name].setdefault(d_level, []).extend(q_items)
        else:
            FALLBACK_TEXT_BANK[r_name] = d_map
except Exception as _e:
    pass

def get_fallback_bank_for_role(role: str, mode: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Returns the organized difficulty-tiered question bank for any role.
    Handles exact matches, synonyms, and sub-domains smoothly.
    """
    bank_source = FALLBACK_MCQ_BANK if mode == "mcq" else FALLBACK_TEXT_BANK
    clean_role = role.strip().lower()

    # 1. Exact match
    for r, diff_map in bank_source.items():
        if r.lower() == clean_role:
            return diff_map

    # 2. Alias mapping
    if "web" in clean_role or "front" in clean_role or "react" in clean_role:
        return bank_source.get("Frontend Developer", bank_source.get("Backend Developer", {}))
    if "data" in clean_role or "analyst" in clean_role:
        return bank_source.get("Data Analyst", bank_source.get("Backend Developer", {}))
    if "machine" in clean_role or "ml" in clean_role or "ai" in clean_role:
        return bank_source.get("Machine Learning Engineer", bank_source.get("Python Developer", {}))
    if "database" in clean_role or "dba" in clean_role or "sql" in clean_role:
        return bank_source.get("Database Administrator", bank_source.get("Backend Developer", {}))
    if "network" in clean_role:
        return bank_source.get("Computer Networks", bank_source.get("Backend Developer", {}))
    if "devops" in clean_role or "cloud" in clean_role or "sre" in clean_role:
        return bank_source.get("DevOps Engineer", bank_source.get("Backend Developer", {}))
    if "security" in clean_role or "cyber" in clean_role:
        return bank_source.get("Computer Networks", bank_source.get("DevOps Engineer", {}))
    if "full" in clean_role or "fullstack" in clean_role:
        return bank_source.get("Backend Developer", bank_source.get("Frontend Developer", {}))
    if "java" in clean_role:
        return bank_source.get("Java Developer", bank_source.get("Backend Developer", {}))
    if "python" in clean_role:
        return bank_source.get("Python Developer", bank_source.get("Backend Developer", {}))
    if "go" in clean_role or "golang" in clean_role or "rust" in clean_role:
        return bank_source.get("Backend Developer", list(bank_source.values())[0])

    # 3. Default to Backend Developer if any other software engineering role
    return bank_source.get("Backend Developer", list(bank_source.values())[0])

