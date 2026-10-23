from typing import Dict, List, Any

EXTRA_MCQ_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Java Developer": {
        "Easy": [
            {
                "question_text": "Which Java collection class allows null values and guarantees insertion order?",
                "topic": "Java Collections Framework & Internals",
                "options": [
                    {"key": "A", "text": "LinkedHashSet"},
                    {"key": "B", "text": "TreeSet"},
                    {"key": "C", "text": "Hashtable"},
                    {"key": "D", "text": "ConcurrentSkipListSet"}
                ],
                "correct_option": "A",
                "explanation": "LinkedHashSet maintains a doubly-linked list running through all of its entries, preserving insertion order while permitting null elements."
            },
            {
                "question_text": "In Java, what happens if a class does not define any constructor?",
                "topic": "Core Java OOP & Polymorphism",
                "options": [
                    {"key": "A", "text": "The compiler automatically generates a public no-argument default constructor"},
                    {"key": "B", "text": "The program will fail to compile with a MissingConstructorException"},
                    {"key": "C", "text": "Objects of the class can only be instantiated through reflection"},
                    {"key": "D", "text": "The JVM creates a singleton instance at class-loading time"}
                ],
                "correct_option": "A",
                "explanation": "If no constructor is explicitly declared in a Java class, the Java compiler automatically supplies a default no-argument constructor that calls super()."
            },
            {
                "question_text": "Which access modifier in Java restricts member visibility exclusively to the containing class and its subclasses?",
                "topic": "Core Java OOP & Polymorphism",
                "options": [
                    {"key": "A", "text": "protected"},
                    {"key": "B", "text": "private"},
                    {"key": "C", "text": "public"},
                    {"key": "D", "text": "default (package-private)"}
                ],
                "correct_option": "A",
                "explanation": "The `protected` modifier allows access within the same package and by subclasses in other packages."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the difference between `Comparable` and `Comparator` interfaces in Java?",
                "topic": "Java Collections Framework & Internals",
                "options": [
                    {"key": "A", "text": "Comparable defines natural ordering via `compareTo()`, while Comparator defines custom external ordering via `compare()`"},
                    {"key": "B", "text": "Comparable works on primitive arrays, while Comparator works on collections"},
                    {"key": "C", "text": "Comparator can only be used with HashMaps, while Comparable works with Lists"},
                    {"key": "D", "text": "Comparable is deprecated in Java 8 in favor of Comparator"}
                ],
                "correct_option": "A",
                "explanation": "Comparable is implemented by the domain class itself (`compareTo(T o)`), whereas Comparator is a separate functional interface (`compare(T o1, T o2)`) providing customizable sort strategies."
            },
            {
                "question_text": "In Java exception handling, what is the key difference between checked and unchecked exceptions?",
                "topic": "Exception Handling (Checked vs Unchecked)",
                "options": [
                    {"key": "A", "text": "Checked exceptions (subclasses of Exception excluding RuntimeException) are verified at compile time; unchecked exceptions (RuntimeException and Error) are not"},
                    {"key": "B", "text": "Unchecked exceptions must always be declared in the `throws` clause of a method"},
                    {"key": "C", "text": "Checked exceptions crash the JVM immediately, while unchecked exceptions are ignored"},
                    {"key": "D", "text": "Unchecked exceptions cannot be caught inside a try-catch block"}
                ],
                "correct_option": "A",
                "explanation": "Checked exceptions are checked by the compiler and must be handled via try-catch or declared in the method signature with `throws`. Unchecked exceptions inherit from RuntimeException."
            },
            {
                "question_text": "What does the `final` keyword indicate when applied to a Java method?",
                "topic": "Core Java OOP & Polymorphism",
                "options": [
                    {"key": "A", "text": "The method cannot be overridden by any subclass"},
                    {"key": "B", "text": "The method cannot accept any input arguments"},
                    {"key": "C", "text": "The method is executed on a dedicated daemon thread"},
                    {"key": "D", "text": "The return value of the method is cached permanently"}
                ],
                "correct_option": "A",
                "explanation": "Declaring a method `final` prevents subclasses from overriding its implementation, ensuring the base behavior remains immutable."
            }
        ],
        "Medium": [
            {
                "question_text": "How does Java's `ConcurrentHashMap` achieve thread-safety without locking the entire table?",
                "topic": "Java Concurrency & Multi-threading",
                "options": [
                    {"key": "A", "text": "In Java 8+, it uses CAS (Compare-And-Swap) for node initialization and synchronizes only on the head node of individual hash buckets"},
                    {"key": "B", "text": "It duplicates the entire map into a thread-local copy on each read/write"},
                    {"key": "C", "text": "It relies entirely on a global ReentrantReadWriteLock"},
                    {"key": "D", "text": "It offloads all update operations to an internal single-threaded executor"}
                ],
                "correct_option": "A",
                "explanation": "Java 8 ConcurrentHashMap abandoned segment locks in favor of lock-free CAS operations for empty buckets and granular `synchronized` blocks on the bucket root node for collisions."
            },
            {
                "question_text": "In Spring Boot, what is the default bean scope when no explicit scope annotation is provided?",
                "topic": "Spring Boot & Dependency Injection",
                "options": [
                    {"key": "A", "text": "singleton"},
                    {"key": "B", "text": "prototype"},
                    {"key": "C", "text": "request"},
                    {"key": "D", "text": "session"}
                ],
                "correct_option": "A",
                "explanation": "The default scope for Spring beans is `singleton`, meaning the Spring IoC container creates and manages exactly one shared instance per ApplicationContext."
            },
            {
                "question_text": "What does Java Generics type erasure mean for runtime execution?",
                "topic": "Java Generics & Type Erasure",
                "options": [
                    {"key": "A", "text": "Type parameters are removed during compilation and replaced by raw types (or upper bounds), with synthetic casts inserted"},
                    {"key": "B", "text": "Generic objects cannot be stored in heap memory"},
                    {"key": "C", "text": "Generics cause the JVM to generate a unique bytecode class file for every distinct type argument"},
                    {"key": "D", "text": "Generic method signatures are deleted from class metadata at runtime"}
                ],
                "correct_option": "A",
                "explanation": "Type erasure ensures backward compatibility with pre-generic Java versions by replacing type parameters with their bounds (or Object) and inserting casts at compile time."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In Hibernate/JPA, what is the 'N+1 Select Problem' and how is it most effectively resolved?",
                "topic": "Hibernate & JPA Persistence",
                "options": [
                    {"key": "A", "text": "Fetching N parent entities triggers N additional secondary queries for child entities; resolved using JOIN FETCH in JPQL or Entity Graphs"},
                    {"key": "B", "text": "A database deadlock caused by executing N concurrent insert queries; resolved by disabling foreign keys"},
                    {"key": "C", "text": "Excessive database connection pooling overhead; resolved by setting pool size to N+1"},
                    {"key": "D", "text": "A caching bug where Hibernate caches N+1 copies of the same entity"}
                ],
                "correct_option": "A",
                "explanation": "The N+1 problem occurs when lazy-loaded associations trigger 1 query for the parent list plus N queries for each element's child collection. JOIN FETCH or @EntityGraph eager-loads them in a single SQL query."
            },
            {
                "question_text": "How does `CompletableFuture.thenCompose()` differ from `CompletableFuture.thenApply()`?",
                "topic": "Java Concurrency & Multi-threading",
                "options": [
                    {"key": "A", "text": "`thenApply()` transforms a value synchronously, whereas `thenCompose()` flattens an asynchronous pipeline returning another CompletableFuture (monadic flatMap)"},
                    {"key": "B", "text": "`thenCompose()` executes on the main UI thread while `thenApply()` runs in ForkJoinPool"},
                    {"key": "C", "text": "`thenApply()` handles exceptions, while `thenCompose()` only handles successful outcomes"},
                    {"key": "D", "text": "`thenCompose()` cannot accept lambda expressions"}
                ],
                "correct_option": "A",
                "explanation": "`thenApply()` behaves like map (returning `CompletableFuture<CompletableFuture<T>>` if the function returns a future), whereas `thenCompose()` behaves like flatMap to avoid nested futures."
            }
        ],
        "Hard": [
            {
                "question_text": "In the Java Memory Model (JMM), how does a write to a `volatile` variable establish a happens-before order with subsequent reads?",
                "topic": "JVM Memory Model & Garbage Collection",
                "options": [
                    {"key": "A", "text": "A write to a volatile variable happens-before every subsequent read of that same volatile variable, flushing preceding CPU store buffers and preventing reordering across memory barriers"},
                    {"key": "B", "text": "It forces the JVM to lock the entire L3 hardware cache until all CPU cores acknowledge the write"},
                    {"key": "C", "text": "It suspends all other running threads until the garbage collector updates pointer references"},
                    {"key": "D", "text": "Volatile writes bypass the L1/L2 cache and write synchronously to swap space"}
                ],
                "correct_option": "A",
                "explanation": "Under the JMM, a volatile write emits a StoreStore and StoreLoad memory barrier, ensuring all preceding writes in program order become visible to any thread that subsequently reads the volatile field."
            },
            {
                "question_text": "In high-throughput microservices using Spring Cloud and Resilience4j, what does a Circuit Breaker do in the HALF_OPEN state?",
                "topic": "Microservices with Spring Cloud",
                "options": [
                    {"key": "A", "text": "It permits a limited trial number of requests to pass through to evaluate whether the downstream service has recovered"},
                    {"key": "B", "text": "It routes 50% of incoming production traffic directly to a dead-letter queue"},
                    {"key": "C", "text": "It rejects 100% of calls with a CallNotPermittedException"},
                    {"key": "D", "text": "It restarts the JVM container to clear exhausted thread pools"}
                ],
                "correct_option": "A",
                "explanation": "In HALF_OPEN state, the circuit breaker allows a configured probe batch of requests. If the failure rate remains below the threshold, it transitions back to CLOSED; otherwise it returns to OPEN."
            }
        ]
    },
    "Frontend Developer": {
        "Easy": [
            {
                "question_text": "In CSS, what is the default value of the `position` property?",
                "topic": "CSS Architecture, Flexbox & Grid",
                "options": [
                    {"key": "A", "text": "static"},
                    {"key": "B", "text": "relative"},
                    {"key": "C", "text": "absolute"},
                    {"key": "D", "text": "fixed"}
                ],
                "correct_option": "A",
                "explanation": "HTML elements have a default CSS position of `static`, meaning they are positioned according to the normal flow of the page."
            },
            {
                "question_text": "Which JavaScript method is used to attach an event handler to a DOM element without overwriting existing handlers?",
                "topic": "JavaScript ES6+ & DOM Manipulation",
                "options": [
                    {"key": "A", "text": "addEventListener()"},
                    {"key": "B", "text": "attachEvent()"},
                    {"key": "C", "text": "onclick()"},
                    {"key": "D", "text": "bindEvent()"}
                ],
                "correct_option": "A",
                "explanation": "`addEventListener()` allows registering multiple independent event listeners on a single DOM element."
            },
            {
                "question_text": "What does CSS `box-sizing: border-box` do when calculating element dimensions?",
                "topic": "CSS Architecture, Flexbox & Grid",
                "options": [
                    {"key": "A", "text": "Includes padding and border within the specified width and height"},
                    {"key": "B", "text": "Excludes padding and border from the width calculation"},
                    {"key": "C", "text": "Adds margin to the element width"},
                    {"key": "D", "text": "Hides any content that overflows the border"}
                ],
                "correct_option": "A",
                "explanation": "With `border-box`, any padding or border is drawn inside the specified width and height, preventing layout breakage when styling containers."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "In React, what is the primary purpose of the `useEffect` hook's dependency array?",
                "topic": "React Hooks & Component Lifecycle",
                "options": [
                    {"key": "A", "text": "To specify when the effect should re-run based on changes in referenced values between renders"},
                    {"key": "B", "text": "To define the CSS transitions used by the component"},
                    {"key": "C", "text": "To register Redux reducers to the component"},
                    {"key": "D", "text": "To prevent child components from re-rendering"}
                ],
                "correct_option": "A",
                "explanation": "React compares values in the dependency array using Object.is between renders. If none have changed, React skips running the effect callback."
            },
            {
                "question_text": "What is the difference between `localStorage` and `sessionStorage` in modern browsers?",
                "topic": "Browser Storage (Cookies, LocalStorage, IndexedDB)",
                "options": [
                    {"key": "A", "text": "localStorage data persists until explicitly cleared; sessionStorage data is purged when the browser tab closes"},
                    {"key": "B", "text": "localStorage has a 4KB quota, while sessionStorage has a 5MB quota"},
                    {"key": "C", "text": "sessionStorage is transmitted automatically with every HTTP request header"},
                    {"key": "D", "text": "localStorage can only store encrypted binary blobs"}
                ],
                "correct_option": "A",
                "explanation": "localStorage persists across browser sessions and tab restarts, whereas sessionStorage data is scoped strictly to the current tab session lifetime."
            },
            {
                "question_text": "How does CSS Flexbox `justify-content` differ from `align-items`?",
                "topic": "Modern CSS (Flexbox, Grid & Container Queries)",
                "options": [
                    {"key": "A", "text": "`justify-content` aligns items along the main axis; `align-items` aligns items along the cross axis"},
                    {"key": "B", "text": "`justify-content` controls font spacing; `align-items` controls box padding"},
                    {"key": "C", "text": "`justify-content` is only valid for grid layouts"},
                    {"key": "D", "text": "`align-items` only works when flex-direction is column"}
                ],
                "correct_option": "A",
                "explanation": "In Flexbox, the main axis direction is set by `flex-direction`. `justify-content` distributes space along this main axis, while `align-items` aligns items along the perpendicular cross axis."
            }
        ],
        "Medium": [
            {
                "question_text": "In React, when should `useCallback` or `useMemo` be employed?",
                "topic": "React Hooks & Component Lifecycle",
                "options": [
                    {"key": "A", "text": "To memoize expensive calculations (`useMemo`) or stable function references (`useCallback`) passed to memoized child components (`React.memo`)"},
                    {"key": "B", "text": "To replace all standard state variables in a component"},
                    {"key": "C", "text": "To force a synchronous re-render before DOM paint"},
                    {"key": "D", "text": "To store credentials securely in memory"}
                ],
                "correct_option": "A",
                "explanation": "Indiscriminate use of `useCallback`/`useMemo` adds memory and comparison overhead. They should be targeted at computationally heavy calculations or preserving reference identity for memoized children."
            },
            {
                "question_text": "What is the Critical Rendering Path in web browsers?",
                "topic": "Critical Rendering Path & Bundle Splitting",
                "options": [
                    {"key": "A", "text": "The sequence of steps: DOM construction -> CSSOM construction -> Render Tree -> Layout -> Paint"},
                    {"key": "B", "text": "The HTTP/2 handshake process before TLS negotiation"},
                    {"key": "C", "text": "The execution of Web Workers off the main thread"},
                    {"key": "D", "text": "The process of bundler minification with Terser"}
                ],
                "correct_option": "A",
                "explanation": "The browser parses HTML into DOM and CSS into CSSOM, combines them into the Render Tree, computes geometric layout coordinates, and paints pixels to the screen."
            },
            {
                "question_text": "What vulnerability does the HTTP header `Content-Security-Policy` (CSP) primarily defend against?",
                "topic": "Frontend Security (XSS, CSRF & CSP)",
                "options": [
                    {"key": "A", "text": "Cross-Site Scripting (XSS) by restricting the domains from which scripts, styles, and assets can be loaded"},
                    {"key": "B", "text": "SQL Injection in database query parameters"},
                    {"key": "C", "text": "Buffer overflow attacks against native browser modules"},
                    {"key": "D", "text": "DNS spoofing on client operating systems"}
                ],
                "correct_option": "A",
                "explanation": "CSP is an effective defense-in-depth security layer that restricts authorized origins for scripts, styles, images, and frame embeddings, mitigating unauthorized script injection."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "What does Core Web Vital metric INP (Interaction to Next Paint) measure?",
                "topic": "Core Web Vitals & Web Performance",
                "options": [
                    {"key": "A", "text": "Overall page responsiveness by observing latency of all user clicks, taps, and keyboard inputs throughout the page lifecycle"},
                    {"key": "B", "text": "The time required to fetch the initial HTML payload over TCP"},
                    {"key": "C", "text": "The duration of JavaScript bundle parsing during boot"},
                    {"key": "D", "text": "The percentage of frames dropped during CSS animations"}
                ],
                "correct_option": "A",
                "explanation": "INP replaced FID in March 2024. It measures the longest interaction latency across input delay, event processing time, and visual presentation delay."
            },
            {
                "question_text": "How do Web Workers communicate with the main JavaScript execution thread?",
                "topic": "Web Workers & Off-Main-Thread Processing",
                "options": [
                    {"key": "A", "text": "Via message passing using `postMessage()` and listening with the `onmessage` event listener"},
                    {"key": "B", "text": "By sharing direct mutable pointers to window.document DOM elements"},
                    {"key": "C", "text": "Through shared global variables in the browser window scope"},
                    {"key": "D", "text": "By writing synchronously to browser cookies"}
                ],
                "correct_option": "A",
                "explanation": "Web Workers run in an isolated background thread without direct DOM access and communicate via asynchronous structured cloning message passing (`postMessage`)."
            }
        ],
        "Hard": [
            {
                "question_text": "How does React 18's Streaming SSR with Selective Hydration improve First Input Delay and Time to Interactive?",
                "topic": "React Hooks & Component Lifecycle",
                "options": [
                    {"key": "A", "text": "It streams HTML chunks wrapped in `<Suspense>` as they resolve, and prioritizes hydrating the specific sub-tree a user interacts with before other components"},
                    {"key": "B", "text": "It converts all React components into static HTML with no client-side JavaScript bundle"},
                    {"key": "C", "text": "It executes React reconciliation exclusively inside Cloudflare Edge Workers"},
                    {"key": "D", "text": "It eliminates the need for virtual DOM comparisons using WebAssembly"}
                ],
                "correct_option": "A",
                "explanation": "Selective Hydration allows React to send early shell HTML and hydrate individual `<Suspense>` boundaries independently, pausing background hydration to prioritize user-clicked elements."
            }
        ]
    },
    "Backend Developer": {
        "Easy": [
            {
                "question_text": "Which HTTP method is defined by RFC 7231 as being both safe and idempotent?",
                "topic": "REST API Design & Idempotency",
                "options": [
                    {"key": "A", "text": "GET"},
                    {"key": "B", "text": "POST"},
                    {"key": "C", "text": "PATCH"},
                    {"key": "D", "text": "CONNECT"}
                ],
                "correct_option": "A",
                "explanation": "GET is safe (does not alter server state) and idempotent (making multiple identical requests produces the same side effect as a single request)."
            },
            {
                "question_text": "What does HTTP status code 403 Forbidden indicate?",
                "topic": "REST API Design & Idempotency",
                "options": [
                    {"key": "A", "text": "The server understands the request and authenticated identity, but refuses authorization to access the resource"},
                    {"key": "B", "text": "The client has not provided valid authentication credentials (unauthorized)"},
                    {"key": "C", "text": "The requested resource could not be found on the server"},
                    {"key": "D", "text": "The server encountered an unhandled internal exception"}
                ],
                "correct_option": "A",
                "explanation": "401 indicates missing or invalid authentication credentials; 403 indicates authentication succeeded but the identity lacks required permissions."
            },
            {
                "question_text": "In relational databases, what does the primary key constraint enforce?",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "options": [
                    {"key": "A", "text": "Unique values for each row and non-null values across the key column(s)"},
                    {"key": "B", "text": "Automatic encryption of table records at rest"},
                    {"key": "C", "text": "Enforces asynchronous replication to standby nodes"},
                    {"key": "D", "text": "Allows null values as long as they are unique"}
                ],
                "correct_option": "A",
                "explanation": "A primary key column uniquely identifies each row in a database table and disallows NULL entries."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the primary architectural difference between an in-memory cache (Redis) and a persistent relational database (PostgreSQL)?",
                "topic": "Distributed Caching Strategies & Redis",
                "options": [
                    {"key": "A", "text": "Redis stores data primarily in RAM providing sub-millisecond key-value operations; PostgreSQL stores structured relational data with disk durability"},
                    {"key": "B", "text": "PostgreSQL does not support transactions, while Redis provides ACID guarantees"},
                    {"key": "C", "text": "Redis only supports integer values"},
                    {"key": "D", "text": "PostgreSQL cannot use B-Tree indexes"}
                ],
                "correct_option": "A",
                "explanation": "Redis operates in-memory for lightning-fast reads and caching, whereas relational databases persist complex transactional schemas to disk."
            },
            {
                "question_text": "What is the difference between synchronous (REST/gRPC) and asynchronous (Kafka/RabbitMQ) microservice communication?",
                "topic": "Microservices Communication (gRPC vs REST)",
                "options": [
                    {"key": "A", "text": "Synchronous calls block the sender until a response is received; asynchronous messaging decouples sender and receiver via message queues"},
                    {"key": "B", "text": "Synchronous communication cannot use JSON payloads"},
                    {"key": "C", "text": "Asynchronous messaging does not support horizontal scaling"},
                    {"key": "D", "text": "REST is asynchronous by default while message queues are synchronous"}
                ],
                "correct_option": "A",
                "explanation": "Synchronous communication creates temporal coupling (sender waits for receiver). Asynchronous message brokers decouple execution and buffer bursts."
            },
            {
                "question_text": "What is the purpose of database connection pooling in high-concurrency backend services?",
                "topic": "Database Indexing (B-Tree, Hash, GIN) & Query Plans",
                "options": [
                    {"key": "A", "text": "To maintain a cache of reusable open database connections and avoid the overhead of TCP handshakes and TLS negotiation per request"},
                    {"key": "B", "text": "To automatically replicate tables across different database vendors"},
                    {"key": "C", "text": "To convert SQL queries into NoSQL document format"},
                    {"key": "D", "text": "To compress database disk blocks in memory"}
                ],
                "correct_option": "A",
                "explanation": "Establishing TCP/TLS connections and database authentication is expensive. Connection pools keep pre-warmed connections ready for immediate reuse."
            }
        ],
        "Medium": [
            {
                "question_text": "In SQL databases, what phenomenon can occur in Read Committed isolation level that is prevented in Repeatable Read?",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "options": [
                    {"key": "A", "text": "Non-repeatable reads (re-reading the same row returns different values committed by another transaction)"},
                    {"key": "B", "text": "Dirty reads of uncommitted data"},
                    {"key": "C", "text": "Complete database write lock contention"},
                    {"key": "D", "text": "Immediate transaction rollback due to schema drift"}
                ],
                "correct_option": "A",
                "explanation": "In Read Committed, each SELECT sees data committed up to that statement. Repeatable Read ensures all SELECTs in a transaction see a consistent snapshot."
            },
            {
                "question_text": "How does the Token Bucket algorithm differ from the Leaky Bucket algorithm for API rate limiting?",
                "topic": "API Rate Limiting & Token Bucket Algorithms",
                "options": [
                    {"key": "A", "text": "Token Bucket allows temporary bursts up to bucket capacity while maintaining an average rate; Leaky Bucket outputs requests at a strictly constant rate"},
                    {"key": "B", "text": "Leaky Bucket allows bursts, while Token Bucket drops all traffic during spikes"},
                    {"key": "C", "text": "Token Bucket cannot be implemented in distributed Redis clusters"},
                    {"key": "D", "text": "Leaky Bucket is only used for TCP network hardware"}
                ],
                "correct_option": "A",
                "explanation": "Token Bucket refills tokens periodically and allows bursts of traffic equal to bucket capacity. Leaky Bucket smooths traffic to a fixed drain rate."
            },
            {
                "question_text": "What is Cache Stampede (or Cache Avalanche) and how can it be mitigated?",
                "topic": "Distributed Caching Strategies & Redis",
                "options": [
                    {"key": "A", "text": "A popular cached key expires, causing thousands of concurrent requests to overwhelm the database simultaneously; mitigated with mutex locking or probabilistic early expiration"},
                    {"key": "B", "text": "Redis runs out of memory and crashes the operating system"},
                    {"key": "C", "text": "A corrupt database index invalidates the entire cache"},
                    {"key": "D", "text": "A network partition between cache replicas"}
                ],
                "correct_option": "A",
                "explanation": "When an expensive hot key expires, simultaneous incoming requests miss the cache and hit the database. Mutex locks (e.g. singleflight) or XFetch probabilistic refresh prevent this."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Why should database indexes on high-cardinality multi-column B-Trees follow the 'Leftmost Prefix' rule?",
                "topic": "Database Indexing (B-Tree, Hash, GIN) & Query Plans",
                "options": [
                    {"key": "A", "text": "The B-Tree is ordered hierarchically by column 1, then column 2, then column 3; queries skipping the first column cannot traverse the tree structure efficiently"},
                    {"key": "B", "text": "Database parsers read WHERE clauses from right to left"},
                    {"key": "C", "text": "The first column is the only column stored in RAM"},
                    {"key": "D", "text": "SQL standards disallow composite indexes with more than two columns"}
                ],
                "correct_option": "A",
                "explanation": "A composite index on (A, B, C) can satisfy queries filtering on (A), (A, B), or (A, B, C), but cannot be utilized effectively for queries filtering solely on (B) or (C)."
            },
            {
                "question_text": "In distributed microservices, how does the Saga Pattern handle distributed transaction rollbacks across microservices without 2-Phase Commit (2PC)?",
                "topic": "System Resilience (Circuit Breaker & Fallback)",
                "options": [
                    {"key": "A", "text": "By executing a sequence of local transactions, where each successful step defines a corresponding compensating transaction executed in reverse order upon failure"},
                    {"key": "B", "text": "By locking all relational tables across all databases simultaneously until all services report success"},
                    {"key": "C", "text": "By converting all microservices into synchronous REST calls within a single thread"},
                    {"key": "D", "text": "By replaying failed transactions indefinitely until the database accepts them"}
                ],
                "correct_option": "A",
                "explanation": "Sagas avoid distributed locks by committing local transactions and executing semantic compensating transactions (e.g. cancelOrder, refundPayment) if a subsequent step fails."
            }
        ],
        "Hard": [
            {
                "question_text": "According to the CAP Theorem, how does a distributed database like Apache Cassandra or Amazon DynamoDB behave during a network partition (P)?",
                "topic": "Database Sharding & Read Replicas",
                "options": [
                    {"key": "A", "text": "It chooses Availability (AP) over strict Consistency, accepting reads and writes on partitioned nodes and resolving conflict later via eventual consistency (last-write-wins or vector clocks)"},
                    {"key": "B", "text": "It shuts down all nodes immediately to prevent any data mutation"},
                    {"key": "C", "text": "It guarantees both instantaneous linearizable consistency and 100% availability during partitions"},
                    {"key": "D", "text": "It routes all network packets through a single hardware proxy"}
                ],
                "correct_option": "A",
                "explanation": "Under the CAP theorem, when a partition occurs, a distributed system must choose between Availability (AP - nodes accept writes, data may diverge temporarily) and Consistency (CP - nodes reject writes if consensus cannot be reached)."
            }
        ]
    },
    "Data Analyst": {
        "Easy": [
            {
                "question_text": "In SQL, which keyword is used to eliminate duplicate rows from a query result set?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "DISTINCT"},
                    {"key": "B", "text": "UNIQUE"},
                    {"key": "C", "text": "DIFFERENT"},
                    {"key": "D", "text": "ISOLATE"}
                ],
                "correct_option": "A",
                "explanation": "`SELECT DISTINCT` filters out identical rows from the returned dataset."
            },
            {
                "question_text": "What does SQL aggregate function `COUNT(column_name)` return when a row has a NULL value in that column?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "It ignores the NULL row and counts only non-null values"},
                    {"key": "B", "text": "It counts NULL as zero"},
                    {"key": "C", "text": "It raises an InvalidDataTypeError"},
                    {"key": "D", "text": "It returns NULL for the entire query"}
                ],
                "correct_option": "A",
                "explanation": "`COUNT(column)` ignores NULL values, whereas `COUNT(*)` counts all rows regardless of NULLs."
            },
            {
                "question_text": "In statistics, what is the median of a dataset?",
                "topic": "A/B Testing, Hypothesis Testing & P-Values",
                "options": [
                    {"key": "A", "text": "The middle value separating the higher half from the lower half when the data is sorted"},
                    {"key": "B", "text": "The arithmetic average of all numbers"},
                    {"key": "C", "text": "The most frequently occurring value in the dataset"},
                    {"key": "D", "text": "The difference between the maximum and minimum values"}
                ],
                "correct_option": "A",
                "explanation": "The median is the 50th percentile, resilient to extreme outliers compared to the arithmetic mean."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "In SQL, what is the difference between `INNER JOIN` and `LEFT JOIN`?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "INNER JOIN returns only rows with matches in both tables; LEFT JOIN returns all rows from the left table and matched rows from the right table (with NULLs for non-matches)"},
                    {"key": "B", "text": "INNER JOIN only works on numerical keys; LEFT JOIN works on string keys"},
                    {"key": "C", "text": "LEFT JOIN deletes rows from the right table that do not match"},
                    {"key": "D", "text": "INNER JOIN produces a cross product Cartesian join"}
                ],
                "correct_option": "A",
                "explanation": "LEFT JOIN preserves all records from the left relation, filling in NULLs when the join condition on the right table is unmet."
            },
            {
                "question_text": "In data modeling, what is the primary characteristic of a Star Schema in a data warehouse?",
                "topic": "Star Schema vs Snowflake Data Modeling",
                "options": [
                    {"key": "A", "text": "A central fact table containing numerical metrics connected directly to de-normalized dimension tables"},
                    {"key": "B", "text": "Multiple normalized dimension tables branching out into sub-dimensions like a snowflake"},
                    {"key": "C", "text": "A single flat CSV table with no relational structure"},
                    {"key": "D", "text": "An unstructured document store using MongoDB collections"}
                ],
                "correct_option": "A",
                "explanation": "Star schema features a centralized fact table referencing denormalized dimension tables, optimizing analytical read queries and simplifying BI joins."
            },
            {
                "question_text": "In Pandas (Python), what does `df.dropna(axis=0)` do to a DataFrame?",
                "topic": "Exploratory Data Analysis with Pandas",
                "options": [
                    {"key": "A", "text": "Drops any row containing at least one missing (NaN/None) value"},
                    {"key": "B", "text": "Drops columns containing missing values"},
                    {"key": "C", "text": "Replaces missing values with zero"},
                    {"key": "D", "text": "Sorts the DataFrame by index"}
                ],
                "correct_option": "A",
                "explanation": "`axis=0` specifies rows; `df.dropna(axis=0)` removes any row with NaN values."
            }
        ],
        "Medium": [
            {
                "question_text": "In SQL, how does `DENSE_RANK()` differ from `RANK()` when window functions encounter tied values?",
                "topic": "SQL Window Functions & Aggregations",
                "options": [
                    {"key": "A", "text": "`RANK()` skips subsequent rank numbers after ties (e.g. 1, 2, 2, 4); `DENSE_RANK()` leaves no gaps (e.g. 1, 2, 2, 3)"},
                    {"key": "B", "text": "`DENSE_RANK()` assigns random ranks to ties to avoid duplicates"},
                    {"key": "C", "text": "`RANK()` can only be used with PostgreSQL"},
                    {"key": "D", "text": "`DENSE_RANK()` requires an unbounded preceding window frame"}
                ],
                "correct_option": "A",
                "explanation": "`RANK()` creates gaps corresponding to the number of tied elements, whereas `DENSE_RANK()` always increments consecutively."
            },
            {
                "question_text": "In A/B testing, what does a p-value of 0.03 mean when testing against a significance threshold (alpha) of 0.05?",
                "topic": "A/B Testing, Hypothesis Testing & P-Values",
                "options": [
                    {"key": "A", "text": "Assuming the null hypothesis is true, there is a 3% probability of observing an effect at least as extreme as the sample data; we reject the null hypothesis"},
                    {"key": "B", "text": "There is a 97% probability that the alternative hypothesis is false"},
                    {"key": "C", "text": "The experiment sample size was too small by 3%"},
                    {"key": "D", "text": "The test result is statistically insignificant"}
                ],
                "correct_option": "A",
                "explanation": "Because p (0.03) < alpha (0.05), the observed difference is statistically significant, justifying rejection of the null hypothesis."
            },
            {
                "question_text": "What is Simpson's Paradox in data analysis?",
                "topic": "Sampling Bias, Survivorship Bias & Simpson's Paradox",
                "options": [
                    {"key": "A", "text": "A trend that appears in several distinct groups disappears or reverses when the groups are aggregated together, caused by a confounding variable"},
                    {"key": "B", "text": "A chart where y-axis scaling distorts true statistical variance"},
                    {"key": "C", "text": "A dataset where mean, median, and mode are identical"},
                    {"key": "D", "text": "A sample where positive instances outnumber negative instances by 100:1"}
                ],
                "correct_option": "A",
                "explanation": "Simpson's Paradox occurs when aggregated data masks or reverses causal sub-group relationships due to unequal sample weights in confounding factors."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "In customer analytics, what is Cohort Retention Analysis used for?",
                "topic": "Cohort Retention Analysis & Churn Modeling",
                "options": [
                    {"key": "A", "text": "Tracking user engagement and churn percentage over standardized time periods (e.g. Day 1, Day 7, Day 30) grouped by signup acquisition date"},
                    {"key": "B", "text": "Predicting database server CPU utilization based on query complexity"},
                    {"key": "C", "text": "Calculating currency exchange rate fluctuations in financial transactions"},
                    {"key": "D", "text": "Estimating network packet loss across geographical regions"}
                ],
                "correct_option": "A",
                "explanation": "Cohort retention measures how long distinct user groups (cohorts defined by common attributes like start week) continue to use the product."
            },
            {
                "question_text": "In SQL, what is the execution difference between a Common Table Expression (CTE) with `WITH` and a Subquery in terms of optimization in modern engines?",
                "topic": "Common Table Expressions (CTEs) vs Views",
                "options": [
                    {"key": "A", "text": "Modern query optimizers inline non-recursive CTEs identically to subqueries, but CTEs provide superior readability and modular multi-referencing"},
                    {"key": "B", "text": "CTEs always write data to physical disk temp files, whereas subqueries never touch disk"},
                    {"key": "C", "text": "Subqueries cannot be combined with JOIN clauses"},
                    {"key": "D", "text": "CTEs cannot utilize database indexes"}
                ],
                "correct_option": "A",
                "explanation": "In PostgreSQL 12+ and modern RDBMS, CTEs are inlined unless explicitly materialized with `WITH ... AS MATERIALIZED`, matching subquery performance."
            }
        ],
        "Hard": [
            {
                "question_text": "How should an analyst detect and address multicollinearity among independent variables in a multiple linear regression model?",
                "topic": "Statistical Outlier Detection & Anomaly Filtering",
                "options": [
                    {"key": "A", "text": "Calculate the Variance Inflation Factor (VIF); if VIF exceeds 5-10, drop collinear features or apply PCA / Ridge regularization"},
                    {"key": "B", "text": "Multiply all input feature columns by a random constant"},
                    {"key": "C", "text": "Switch from Mean Absolute Error to R-squared loss"},
                    {"key": "D", "text": "Remove all rows with negative values from the training dataset"}
                ],
                "correct_option": "A",
                "explanation": "High VIF indicates independent variables are correlated with each other, inflating coefficient variance and destabilizing model interpretability."
            }
        ]
    },
    "DevOps Engineer": {
        "Easy": [
            {
                "question_text": "Which Docker command is used to display all currently running and stopped containers?",
                "topic": "Docker Containerization & Multi-stage Builds",
                "options": [
                    {"key": "A", "text": "docker ps -a"},
                    {"key": "B", "text": "docker list --all"},
                    {"key": "C", "text": "docker images"},
                    {"key": "D", "text": "docker status"}
                ],
                "correct_option": "A",
                "explanation": "`docker ps` shows running containers; adding `-a` (or `--all`) displays stopped and exited containers as well."
            },
            {
                "question_text": "In Linux, which command changes file permissions?",
                "topic": "Linux Systems Administration & Shell Scripting",
                "options": [
                    {"key": "A", "text": "chmod"},
                    {"key": "B", "text": "chown"},
                    {"key": "C", "text": "chperm"},
                    {"key": "D", "text": "sudo"}
                ],
                "correct_option": "A",
                "explanation": "`chmod` (change mode) sets read, write, and execute permissions on files and directories."
            },
            {
                "question_text": "In Git, which command creates and switches to a new branch simultaneously?",
                "topic": "CI/CD Pipelines & GitHub Actions Workflows",
                "options": [
                    {"key": "A", "text": "git checkout -b <branch-name>"},
                    {"key": "B", "text": "git branch --switch <branch-name>"},
                    {"key": "C", "text": "git commit -b <branch-name>"},
                    {"key": "D", "text": "git merge --new <branch-name>"}
                ],
                "correct_option": "A",
                "explanation": "`git checkout -b <branch>` (or modern `git switch -c <branch>`) creates the branch and checks it out."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Why are multi-stage Docker builds recommended for compiled languages (Go, Java, Rust)?",
                "topic": "Docker Containerization & Multi-stage Builds",
                "options": [
                    {"key": "A", "text": "They allow compiling code in a heavy build container and copying only the final binary into a minimal runtime image, reducing image size and attack surface"},
                    {"key": "B", "text": "They allow a container to run multiple operating systems concurrently"},
                    {"key": "C", "text": "They automatically push images to Docker Hub during build"},
                    {"key": "D", "text": "They prevent containers from using CPU cgroups"}
                ],
                "correct_option": "A",
                "explanation": "Multi-stage builds leave behind SDKs, compilers, and intermediate build artifacts, resulting in lean production images (e.g. alpine or distroless)."
            },
            {
                "question_text": "In Kubernetes, what is the purpose of a `ConfigMap` versus a `Secret`?",
                "topic": "Kubernetes Pods, Deployments & DaemonSets",
                "options": [
                    {"key": "A", "text": "ConfigMap stores non-confidential configuration key-values in plaintext; Secret stores sensitive data (passwords, tokens) encoded in base64 with RBAC restrictions"},
                    {"key": "B", "text": "ConfigMap is only used for networking, while Secret is used for storage volumes"},
                    {"key": "C", "text": "Secret can only be read by the root user of the host machine"},
                    {"key": "D", "text": "ConfigMaps cannot be mounted as file volumes"}
                ],
                "correct_option": "A",
                "explanation": "ConfigMaps decouple environment configuration from container images, while Secrets add access controls and base64 encoding (or encryption at rest in etcd)."
            },
            {
                "question_text": "What is the function of an Amazon AWS Security Group in a VPC?",
                "topic": "Cloud Networking (VPC, Subnets, Security Groups)",
                "options": [
                    {"key": "A", "text": "A stateful virtual firewall operating at the instance/ENI level controlling inbound and outbound traffic"},
                    {"key": "B", "text": "A stateless subnet-level packet filter"},
                    {"key": "C", "text": "An automated DNS load balancer"},
                    {"key": "D", "text": "A hardware VPN connection to on-premises data centers"}
                ],
                "correct_option": "A",
                "explanation": "Security Groups are stateful firewalls applied to ENIs; return traffic is automatically allowed regardless of outbound rules."
            }
        ],
        "Medium": [
            {
                "question_text": "In Terraform, what does `terraform state rm` do?",
                "topic": "Infrastructure as Code (Terraform & State Locking)",
                "options": [
                    {"key": "A", "text": "Removes a resource from Terraform state tracking without destroying the physical cloud infrastructure"},
                    {"key": "B", "text": "Terminates the resource in AWS and deletes its state"},
                    {"key": "C", "text": "Rolls back Terraform configuration to the previous Git commit"},
                    {"key": "D", "text": "Clears all cached Terraform provider plugins"}
                ],
                "correct_option": "A",
                "explanation": "`terraform state rm` stops Terraform from managing a resource, leaving the real infrastructure intact in the cloud provider."
            },
            {
                "question_text": "In Kubernetes, what is the role of a `LivenessProbe` versus a `ReadinessProbe`?",
                "topic": "Kubernetes Pods, Deployments & DaemonSets",
                "options": [
                    {"key": "A", "text": "LivenessProbe restarts the container if it fails; ReadinessProbe removes the pod from service endpoints until it passes"},
                    {"key": "B", "text": "LivenessProbe checks memory, while ReadinessProbe checks CPU"},
                    {"key": "C", "text": "ReadinessProbe runs only once when the container boots; LivenessProbe never runs"},
                    {"key": "D", "text": "LivenessProbe stops the Kubernetes master node if failing"}
                ],
                "correct_option": "A",
                "explanation": "If a liveness probe fails, kubelet kills and restarts the container. If a readiness probe fails, the pod is isolated from ingress traffic until healthy."
            },
            {
                "question_text": "How does GitOps (e.g. ArgoCD or Flux) enforce continuous delivery in Kubernetes clusters?",
                "topic": "GitOps Principles & ArgoCD",
                "options": [
                    {"key": "A", "text": "By using Git as the single source of truth and having an in-cluster agent continuously pull and reconcile differences between Git manifests and live cluster state"},
                    {"key": "B", "text": "By pushing Docker images directly into Kubernetes worker node RAM via SSH"},
                    {"key": "C", "text": "By disabling automated testing in continuous integration pipelines"},
                    {"key": "D", "text": "By generating ephemeral Kubernetes clusters for every pull request"}
                ],
                "correct_option": "A",
                "explanation": "GitOps uses declarative Git repositories as the desired state and reconciliation controllers inside the cluster to detect and correct configuration drift automatically."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "How does Prometheus scrape metrics from application services?",
                "topic": "Observability & Monitoring (Prometheus & Grafana)",
                "options": [
                    {"key": "A", "text": "Via an active pull model over HTTP periodically querying `/metrics` endpoints discovered through service discovery"},
                    {"key": "B", "text": "Via continuous UDP packet push streams sent by every container"},
                    {"key": "C", "text": "By reading Linux kernel syslog files directly from the host filesystem"},
                    {"key": "D", "text": "By querying database slow query logs"}
                ],
                "correct_option": "A",
                "explanation": "Prometheus uses pull-based scraping over HTTP, allowing central control over scrape intervals and health monitoring of metric endpoints."
            },
            {
                "question_text": "In Terraform state management, why is State Locking with AWS DynamoDB or Consul critical in team environments?",
                "topic": "Infrastructure as Code (Terraform & State Locking)",
                "options": [
                    {"key": "A", "text": "To prevent concurrent `terraform apply` executions from corrupting the state file or deploying conflicting resources"},
                    {"key": "B", "text": "To encrypt Terraform variables using asymmetric keys"},
                    {"key": "C", "text": "To compress terraform plans before upload to S3"},
                    {"key": "D", "text": "To bypass AWS IAM permissions checks"}
                ],
                "correct_option": "A",
                "explanation": "State locking acquires a mutex lock during mutations, ensuring that two CI jobs or engineers cannot modify state simultaneously."
            }
        ],
        "Hard": [
            {
                "question_text": "What is the primary advantage of a Service Mesh (such as Istio or Linkerd) over traditional application-level libraries for microservice traffic management?",
                "topic": "Zero-Downtime Deployments (Blue-Green & Canary)",
                "options": [
                    {"key": "A", "text": "It offloads mTLS encryption, traffic routing, retry policies, and telemetry to sidecar proxies (Envoy) transparently without application code changes"},
                    {"key": "B", "text": "It replaces Kubernetes ingress controllers entirely with DNS records"},
                    {"key": "C", "text": "It compiles application source code directly into Linux kernel eBPF bytecode"},
                    {"key": "D", "text": "It eliminates the need for containers by virtualizing CPU hardware"}
                ],
                "correct_option": "A",
                "explanation": "Service meshes run Envoy sidecars alongside each pod, handling mutual TLS (mTLS), circuit breaking, fault injection, and distributed tracing uniformly across polyglot microservices."
            }
        ]
    },
    "Machine Learning Engineer": {
        "Easy": [
            {
                "question_text": "In machine learning, what is the primary goal of Supervised Learning compared to Unsupervised Learning?",
                "topic": "Supervised vs Unsupervised Learning Algorithms",
                "options": [
                    {"key": "A", "text": "Supervised learning trains models on labeled input-output pairs to predict target outcomes; unsupervised learning discovers latent patterns from unlabeled data"},
                    {"key": "B", "text": "Supervised learning requires human code reviewers to approve every model prediction"},
                    {"key": "C", "text": "Supervised learning only works on image data"},
                    {"key": "D", "text": "Unsupervised learning always achieves 100% accuracy"}
                ],
                "correct_option": "A",
                "explanation": "Supervised learning maps features X to known labels Y. Unsupervised learning clusters or decomposes unlabeled feature sets."
            },
            {
                "question_text": "What does a high training accuracy combined with very low validation accuracy typically indicate?",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "options": [
                    {"key": "A", "text": "Overfitting (high variance), where the model memorizes training noise rather than generalizing"},
                    {"key": "B", "text": "Underfitting (high bias), where the model is too simple"},
                    {"key": "C", "text": "The learning rate is too low"},
                    {"key": "D", "text": "The test set has no variance"}
                ],
                "correct_option": "A",
                "explanation": "Overfitting occurs when a high-capacity model fits training data quirks and noise, degrading out-of-sample generalization performance."
            },
            {
                "question_text": "Which metric is the harmonic mean of Precision and Recall?",
                "topic": "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
                "options": [
                    {"key": "A", "text": "F1-Score"},
                    {"key": "B", "text": "ROC-AUC"},
                    {"key": "C", "text": "Mean Squared Error (MSE)"},
                    {"key": "D", "text": "Log-Loss"}
                ],
                "correct_option": "A",
                "explanation": "F1-Score is defined as `2 * (Precision * Recall) / (Precision + Recall)`, balancing precision and recall on imbalanced datasets."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "How does L1 regularization (Lasso) differ from L2 regularization (Ridge) in linear models?",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "options": [
                    {"key": "A", "text": "L1 penalizes the sum of absolute weights, driving irrelevant feature weights to exact zero (sparse feature selection); L2 penalizes squared weights, shrinking them smoothly"},
                    {"key": "B", "text": "L2 creates exact zero weights while L1 does not"},
                    {"key": "C", "text": "L1 can only be used with neural networks, while L2 is for linear regression"},
                    {"key": "D", "text": "L2 regularization prevents gradient descent from converging"}
                ],
                "correct_option": "A",
                "explanation": "The diamond constraint geometry of L1 regularization intersects axes at exact zeros, performing automatic sparse feature selection."
            },
            {
                "question_text": "What is the primary function of Principal Component Analysis (PCA)?",
                "topic": "Feature Engineering & Dimensionality Reduction (PCA)",
                "options": [
                    {"key": "A", "text": "An unsupervised orthogonal linear transformation projecting data onto directions of maximum variance to reduce dimensionality"},
                    {"key": "B", "text": "A supervised classification algorithm for categorical features"},
                    {"key": "C", "text": "A hyperparameter tuning method for neural networks"},
                    {"key": "D", "text": "A method to generate synthetic training data"}
                ],
                "correct_option": "A",
                "explanation": "PCA computes the eigenvectors of the covariance matrix to project high-dimensional data onto orthogonal principal components of maximum variance."
            },
            {
                "question_text": "Why is cross-validation (e.g. K-Fold) preferred over a single train/test split when evaluating models on small or moderate datasets?",
                "topic": "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
                "options": [
                    {"key": "A", "text": "It provides a more reliable, lower-variance estimate of generalization error by training and evaluating on all folds"},
                    {"key": "B", "text": "It prevents the model from using gradient descent"},
                    {"key": "C", "text": "It reduces the total computational time by a factor of K"},
                    {"key": "D", "text": "It eliminates the need for test labels"}
                ],
                "correct_option": "A",
                "explanation": "K-fold cross-validation rotates training and test folds across the entire dataset, mitigating sample bias and split variance."
            }
        ],
        "Medium": [
            {
                "question_text": "In deep learning, what problem does the Rectified Linear Unit (ReLU) activation function solve compared to Sigmoid/Tanh?",
                "topic": "Neural Network Architectures & Backpropagation",
                "options": [
                    {"key": "A", "text": "It mitigates the vanishing gradient problem for positive inputs because its derivative is a constant 1, enabling deeper networks to train efficiently"},
                    {"key": "B", "text": "It guarantees that weights never exceed 1.0"},
                    {"key": "C", "text": "It prevents dead neurons completely under negative inputs"},
                    {"key": "D", "text": "It eliminates the need for backpropagation"}
                ],
                "correct_option": "A",
                "explanation": "Sigmoid and tanh saturate at their extremes with derivatives approaching zero, causing gradients to vanish. ReLU retains a constant gradient of 1 for positive activations."
            },
            {
                "question_text": "How does the Adam optimizer combine the benefits of AdaGrad and RMSProp?",
                "topic": "Gradient Descent & Optimization (Adam, SGD)",
                "options": [
                    {"key": "A", "text": "It computes adaptive learning rates for each parameter using exponentially decaying averages of past gradients (momentum) and past squared gradients"},
                    {"key": "B", "text": "It switches between L1 and L2 regularization every epoch"},
                    {"key": "C", "text": "It computes exact second-order Hessian matrix inverses in O(1) time"},
                    {"key": "D", "text": "It trains multiple models on different GPUs synchronously"}
                ],
                "correct_option": "A",
                "explanation": "Adam (Adaptive Moment Estimation) tracks first-order moments (mean/momentum) and uncentered second-order moments (variance) with bias correction."
            },
            {
                "question_text": "What technique is commonly used to address severe class imbalance when training binary fraud detection models?",
                "topic": "Handling Class Imbalance (SMOTE, Focal Loss)",
                "options": [
                    {"key": "A", "text": "SMOTE (Synthetic Minority Over-sampling Technique) or Focal Loss down-weighting easy negative examples"},
                    {"key": "B", "text": "Removing the majority class completely from the training set"},
                    {"key": "C", "text": "Increasing learning rate to 10.0"},
                    {"key": "D", "text": "Evaluating accuracy exclusively as the optimization metric"}
                ],
                "correct_option": "A",
                "explanation": "SMOTE interpolates synthetic minority points in feature space, while Focal Loss dynamically scales loss to focus training on hard negative edge cases."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "What is Concept Drift in production machine learning systems, and how is it detected?",
                "topic": "Data Drift, Concept Drift & Model Monitoring",
                "options": [
                    {"key": "A", "text": "A shift in the statistical relationship between input features X and target label Y over time; detected via monitoring ground-truth metrics, PSI, and Kolmogorov-Smirnov statistical tests"},
                    {"key": "B", "text": "A memory leak in the model inference server"},
                    {"key": "C", "text": "A bug where training data is formatted as strings instead of floats"},
                    {"key": "D", "text": "A hardware GPU clock frequency drop under high thermal load"}
                ],
                "correct_option": "A",
                "explanation": "Concept drift represents changes in underlying real-world dynamics P(Y|X). Monitoring data drift and model accuracy against newly labeled production data identifies when retraining is needed."
            },
            {
                "question_text": "How does Random Forest reduce model variance compared to individual Decision Trees?",
                "topic": "Ensemble Learning (Random Forest, XGBoost)",
                "options": [
                    {"key": "A", "text": "By averaging predictions across an ensemble of decorrelated trees trained on bootstrap samples with random feature subset selection (Bagging)"},
                    {"key": "B", "text": "By sequentially boosting errors of previous trees with gradient descent"},
                    {"key": "C", "text": "By pruning all trees to a maximum depth of 1 (decision stumps)"},
                    {"key": "D", "text": "By standardizing all input features to unit normal distribution"}
                ],
                "correct_option": "A",
                "explanation": "Random Forest builds B unpruned trees using bootstrap aggregation (bagging) and random feature subsampling, lowering variance without increasing bias."
            }
        ],
        "Hard": [
            {
                "question_text": "How does Knowledge Distillation optimize deep neural network inference latency for production edge deployment?",
                "topic": "Model Deployment & Inference Latency Optimization",
                "options": [
                    {"key": "A", "text": "A compact student model is trained to mimic the soft probability distributions (dark knowledge) produced by a larger, high-capacity teacher ensemble"},
                    {"key": "B", "text": "It converts 32-bit floating point weights into analog audio waveforms"},
                    {"key": "C", "text": "It disables all non-linear activation layers in the student network"},
                    {"key": "D", "text": "It recompiles PyTorch models into bash scripts"}
                ],
                "correct_option": "A",
                "explanation": "Knowledge distillation uses softened softmax logits from a cumbersome teacher model to transfer rich dark knowledge into a lightweight student model with minimal accuracy loss."
            }
        ]
    },
    "Database Administrator": {
        "Easy": [
            {
                "question_text": "What does ACID stand for in database transaction management?",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "options": [
                    {"key": "A", "text": "Atomicity, Consistency, Isolation, Durability"},
                    {"key": "B", "text": "Access, Control, Indexing, Data"},
                    {"key": "C", "text": "Aggregation, Clustering, Integrity, Distribution"},
                    {"key": "D", "text": "Authentication, Cryptography, Isolation, Duplication"}
                ],
                "correct_option": "A",
                "explanation": "ACID is the benchmark standard for reliable transaction processing in database management systems."
            },
            {
                "question_text": "Which SQL command is used to add a new column to an existing table?",
                "topic": "Relational Schema Design & 3NF Normalization",
                "options": [
                    {"key": "A", "text": "ALTER TABLE <table_name> ADD COLUMN <column_name> <data_type>;"},
                    {"key": "B", "text": "UPDATE TABLE <table_name> INSERT COLUMN <column_name>;"},
                    {"key": "C", "text": "MODIFY TABLE <table_name> CREATE <column_name>;"},
                    {"key": "D", "text": "EXTEND TABLE <table_name> WITH <column_name>;"}
                ],
                "correct_option": "A",
                "explanation": "`ALTER TABLE ... ADD COLUMN` modifies the schema definition of an existing database table."
            },
            {
                "question_text": "What is the primary role of a database Foreign Key?",
                "topic": "Relational Schema Design & 3NF Normalization",
                "options": [
                    {"key": "A", "text": "To enforce referential integrity between columns in two relational tables"},
                    {"key": "B", "text": "To automatically encrypt confidential table data"},
                    {"key": "C", "text": "To replicate tables to foreign cloud regions"},
                    {"key": "D", "text": "To speed up full table scans"}
                ],
                "correct_option": "A",
                "explanation": "Foreign keys ensure that relationships between table records remain valid and prevent orphan records."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is the difference between a Clustered Index and a Non-Clustered Index?",
                "topic": "B-Tree vs Hash vs Bitmap Index Architecture",
                "options": [
                    {"key": "A", "text": "A clustered index dictates the physical sorting order of table rows on disk (only 1 per table); a non-clustered index stores pointers to row locations"},
                    {"key": "B", "text": "A clustered index can only index integer columns"},
                    {"key": "C", "text": "Non-clustered indexes cannot be used in WHERE clauses"},
                    {"key": "D", "text": "A table can have up to 100 clustered indexes"}
                ],
                "correct_option": "A",
                "explanation": "Because physical disk rows can only be arranged in one sequential order, each table can possess at most one clustered index."
            },
            {
                "question_text": "In PostgreSQL, what is the purpose of the `VACUUM` command?",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "options": [
                    {"key": "A", "text": "Reclaims storage occupied by dead row tuples resulting from UPDATEs and DELETEs (MVCC bloat) and updates visibility maps"},
                    {"key": "B", "text": "Deletes all tables in the public schema"},
                    {"key": "C", "text": "Converts all B-Tree indexes into Hash indexes"},
                    {"key": "D", "text": "Compresses database backup files with gzip"}
                ],
                "correct_option": "A",
                "explanation": "PostgreSQL MVCC writes new row versions on updates. `VACUUM` cleans dead tuples, preventing table bloat and transaction ID wraparound."
            },
            {
                "question_text": "What is the purpose of Point-in-Time Recovery (PITR)?",
                "topic": "Backup Strategies, Point-in-Time Recovery (PITR)",
                "options": [
                    {"key": "A", "text": "Restoring a database to the exact millisecond before a catastrophic failure or erroneous data deletion by replaying WAL logs on a base backup"},
                    {"key": "B", "text": "Predicting database query response times using statistical benchmarks"},
                    {"key": "C", "text": "Reverting schema migrations without rollbacks"},
                    {"key": "D", "text": "Exporting CSV snapshots of tables every hour"}
                ],
                "correct_option": "A",
                "explanation": "PITR combines a baseline physical backup with continuous WAL archiving, allowing DBAs to restore to any chosen microsecond."
            }
        ],
        "Medium": [
            {
                "question_text": "In PostgreSQL query execution plans, what is the difference between `Seq Scan` and `Index Scan`?",
                "topic": "Query Execution Plans & EXPLAIN ANALYZE",
                "options": [
                    {"key": "A", "text": "Seq Scan reads all table disk pages sequentially from beginning to end; Index Scan traverses a B-Tree index to locate and fetch specific heap tuples"},
                    {"key": "B", "text": "Seq Scan only runs on foreign tables"},
                    {"key": "C", "text": "Index Scan is always slower than Seq Scan"},
                    {"key": "D", "text": "Seq Scan requires an explicit index on primary keys"}
                ],
                "correct_option": "A",
                "explanation": "For selective filters, Index Scan traverses the tree to fetch matching rows. For large table fractions, Seq Scan is faster due to sequential disk I/O."
            },
            {
                "question_text": "What is a Deadlock in relational databases, and how do database engines resolve it?",
                "topic": "Locking Mechanisms & Deadlock Resolution",
                "options": [
                    {"key": "A", "text": "Two transactions hold locks that each other requires to proceed, creating a circular wait; the engine detects the cycle and aborts one transaction (victim)"},
                    {"key": "B", "text": "A database corruption where tables cannot be read from disk"},
                    {"key": "C", "text": "A state where the WAL log disk fills up to 100% capacity"},
                    {"key": "D", "text": "A network timeout between client and database server"}
                ],
                "correct_option": "A",
                "explanation": "A deadlock cycle cannot resolve without intervention. The deadlock detector identifies the wait-for graph cycle and rolls back one transaction."
            },
            {
                "question_text": "How does database Table Partitioning (declarative partitioning) improve performance on massive multi-terabyte tables?",
                "topic": "Table Partitioning & Sharding Techniques",
                "options": [
                    {"key": "A", "text": "Enables Partition Pruning, allowing the query planner to bypass scanning irrelevant partition tables entirely based on query filter ranges"},
                    {"key": "B", "text": "Eliminates the need for primary key constraints"},
                    {"key": "C", "text": "Stores table partitions across separate database engines like MySQL and Oracle"},
                    {"key": "D", "text": "Disables ACID logging for partition tables"}
                ],
                "correct_option": "A",
                "explanation": "Partitioning (e.g. by date range) allows partition pruning, where queries filtering on date read only matching sub-tables, skipping 99% of data."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "How does Asynchronous Streaming Replication differ from Synchronous Replication in high-availability database clusters?",
                "topic": "Database Replication (Synchronous vs Asynchronous)",
                "options": [
                    {"key": "A", "text": "Synchronous replication guarantees zero data loss (RPO=0) by waiting for standby nodes to acknowledge WAL write before committing; asynchronous commits immediately on primary with low latency"},
                    {"key": "B", "text": "Asynchronous replication does not write WAL logs"},
                    {"key": "C", "text": "Synchronous replication cannot use read replicas"},
                    {"key": "D", "text": "Asynchronous replication operates exclusively over HTTP"}
                ],
                "correct_option": "A",
                "explanation": "Synchronous replication guarantees durability across nodes at the cost of write latency. Asynchronous replication maximizes write performance but risks replication lag."
            },
            {
                "question_text": "What is Connection Pool Exhaustion in high-traffic applications, and what is the best architectural mitigation?",
                "topic": "Connection Pooling & Resource Limits",
                "options": [
                    {"key": "A", "text": "All available database server connections are saturated by long-running queries or idle client sessions; mitigated by setting query statement timeouts, sizing pool to match CPU cores, and deploying an external proxy (PgBouncer)"},
                    {"key": "B", "text": "Increasing max_connections in postgresql.conf to 50,000"},
                    {"key": "C", "text": "Disabling database connection authentication"},
                    {"key": "D", "text": "Restarting the database every 10 minutes"}
                ],
                "correct_option": "A",
                "explanation": "High database connections degrade performance due to process context-switching. Transaction-level pooling proxies like PgBouncer multiplex thousands of client connections onto a small worker pool."
            }
        ],
        "Hard": [
            {
                "question_text": "How does PostgreSQL implement Multi-Version Concurrency Control (MVCC) at the storage engine level without row-level read locks?",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "options": [
                    {"key": "A", "text": "Every heap tuple stores `xmin` (creating transaction ID) and `xmax` (deleting/updating transaction ID) headers, allowing queries to read a snapshot of valid row versions without blocking writers"},
                    {"key": "B", "text": "By duplicating the entire database schema into private memory buffers for each active connection"},
                    {"key": "C", "text": "By pausing background write operations during SELECT statements"},
                    {"key": "D", "text": "By compiling SQL statements into immutable binary tree files"}
                ],
                "correct_option": "A",
                "explanation": "MVCC creates new tuple versions instead of mutating rows in place. Readers check `xmin`/`xmax` against their transaction snapshot, guaranteeing readers never block writers and writers never block readers."
            }
        ]
    },
    "Computer Networks": {
        "Easy": [
            {
                "question_text": "Which layer of the OSI model is responsible for logical IP addressing and packet routing across networks?",
                "topic": "OSI Model vs TCP/IP Protocol Suite",
                "options": [
                    {"key": "A", "text": "Network Layer (Layer 3)"},
                    {"key": "B", "text": "Data Link Layer (Layer 2)"},
                    {"key": "C", "text": "Transport Layer (Layer 4)"},
                    {"key": "D", "text": "Session Layer (Layer 5)"}
                ],
                "correct_option": "A",
                "explanation": "Layer 3 (Network Layer) handles logical IP addressing, packet forwarding, and path selection across interconnected networks."
            },
            {
                "question_text": "What is the primary difference between TCP and UDP protocols?",
                "topic": "UDP vs TCP Protocol Characteristics",
                "options": [
                    {"key": "A", "text": "TCP is connection-oriented with guaranteed in-order delivery and flow control; UDP is connectionless and lightweight without retransmissions"},
                    {"key": "B", "text": "UDP guarantees packet delivery while TCP does not"},
                    {"key": "C", "text": "TCP can only transmit plaintext data"},
                    {"key": "D", "text": "UDP is restricted to local area networks (LAN)"}
                ],
                "correct_option": "A",
                "explanation": "TCP provides reliable, sequenced byte streams via handshakes, acknowledgments, and retransmissions. UDP provides fast, stateless datagram transmission."
            },
            {
                "question_text": "What is the standard port number for HTTPS (Hypertext Transfer Protocol Secure)?",
                "topic": "TLS/SSL Handshake & Symmetric/Asymmetric Encryption",
                "options": [
                    {"key": "A", "text": "443"},
                    {"key": "B", "text": "80"},
                    {"key": "C", "text": "22"},
                    {"key": "D", "text": "53"}
                ],
                "correct_option": "A",
                "explanation": "Port 443 is assigned by IANA for encrypted HTTPS traffic. Port 80 is HTTP, 22 is SSH, and 53 is DNS."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "In IP networking, what does a Subnet Mask (such as 255.255.255.0 or /24) determine?",
                "topic": "Subnetting, CIDR & IP Addressing",
                "options": [
                    {"key": "A", "text": "It divides the 32-bit IPv4 address into the network prefix portion and the host portion"},
                    {"key": "B", "text": "It encrypts network packets between switches"},
                    {"key": "C", "text": "It specifies the MAC address of the default gateway router"},
                    {"key": "D", "text": "It limits maximum network transmission speed to 255 Mbps"}
                ],
                "correct_option": "A",
                "explanation": "The subnet mask uses contiguous 1-bits to demarcate the network identifier from the individual host identifier in an IP address."
            },
            {
                "question_text": "What is the function of the Address Resolution Protocol (ARP)?",
                "topic": "OSI Model vs TCP/IP Protocol Suite",
                "options": [
                    {"key": "A", "text": "Maps a known Layer 3 IP address to a physical Layer 2 MAC address on the local network link"},
                    {"key": "B", "text": "Resolves domain names into public IP addresses"},
                    {"key": "C", "text": "Assigns dynamic IP addresses to new network devices"},
                    {"key": "D", "text": "Encrypts TCP payloads before transmission"}
                ],
                "correct_option": "A",
                "explanation": "ARP broadcasts on the local Layer 2 broadcast domain to discover the MAC address corresponding to a given target IP address."
            },
            {
                "question_text": "What type of DNS record maps a domain name directly to an IPv4 address?",
                "topic": "DNS Resolution Architecture & Record Types",
                "options": [
                    {"key": "A", "text": "A Record"},
                    {"key": "B", "text": "CNAME Record"},
                    {"key": "C", "text": "MX Record"},
                    {"key": "D", "text": "AAAA Record"}
                ],
                "correct_option": "A",
                "explanation": "An 'A' record maps a hostname to an IPv4 address. 'AAAA' maps to IPv6; 'CNAME' aliases one hostname to another."
            }
        ],
        "Medium": [
            {
                "question_text": "How does the TCP 3-Way Handshake establish a reliable connection between client and server?",
                "topic": "TCP 3-Way Handshake, Flow Control & Congestion Control",
                "options": [
                    {"key": "A", "text": "1. Client sends SYN(seq=x) -> 2. Server replies SYN(seq=y), ACK(x+1) -> 3. Client sends ACK(y+1); establishing synchronized sequence numbers in both directions"},
                    {"key": "B", "text": "Client sends DATA -> Server replies OK -> Client disconnects"},
                    {"key": "C", "text": "Client sends TLS ClientHello -> Server sends Certificate -> Client verifies signature"},
                    {"key": "D", "text": "Client sends UDP ping -> Server replies with IP address"}
                ],
                "correct_option": "A",
                "explanation": "The SYN -> SYN-ACK -> ACK handshake establishes Initial Sequence Numbers (ISNs) and buffer parameters for full-duplex byte stream transmission."
            },
            {
                "question_text": "What is the primary difference between Network Address Translation (NAT) and Port Address Translation (PAT / NAT Overload)?",
                "topic": "Network Address Translation (NAT) & PAT",
                "options": [
                    {"key": "A", "text": "Static NAT maps private IPs to public IPs one-to-one; PAT maps multiple private IPs to a single public IP by tracking unique Layer 4 source port numbers"},
                    {"key": "B", "text": "NAT works only on IPv6 addresses, while PAT works on IPv4"},
                    {"key": "C", "text": "PAT requires hardware VPN routers"},
                    {"key": "D", "text": "NAT changes MAC addresses, while PAT changes DNS records"}
                ],
                "correct_option": "A",
                "explanation": "PAT multiplexes thousands of private host connections onto a single public IP address by assigning unique ephemeral TCP/UDP source ports."
            },
            {
                "question_text": "In Layer 2 Ethernet networks, what problem does Spanning Tree Protocol (STP) prevent?",
                "topic": "VLANs, Switching & Spanning Tree Protocol (STP)",
                "options": [
                    {"key": "A", "text": "Bridge loops and catastrophic broadcast radiation storms caused by redundant physical links between switches"},
                    {"key": "B", "text": "IP address exhaustion in DHCP pools"},
                    {"key": "C", "text": "Buffer overflow attacks on router CPU interfaces"},
                    {"key": "D", "text": "Unauthorized packet sniffing by unmanaged hosts"}
                ],
                "correct_option": "A",
                "explanation": "STP builds a loop-free logical topology by disabling redundant paths into blocking states, activating them automatically if the root bridge or active link fails."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "How does HTTP/2 multiplexing improve page load performance over HTTP/1.1?",
                "topic": "HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)",
                "options": [
                    {"key": "A", "text": "It breaks requests and responses into binary frames multiplexed over a single persistent TCP connection, eliminating head-of-line blocking at the application layer"},
                    {"key": "B", "text": "It compresses HTML text using gzip on the client"},
                    {"key": "C", "text": "It bypasses TCP handshakes by using raw Ethernet frames"},
                    {"key": "D", "text": "It opens 100 parallel TCP sockets per browser tab"}
                ],
                "correct_option": "A",
                "explanation": "HTTP/2 interleaves request/response streams over one connection using binary framing and HPACK header compression, avoiding HTTP/1.1 pipeline head-of-line blocking."
            },
            {
                "question_text": "Why does HTTP/3 switch from TCP to QUIC over UDP at the transport layer?",
                "topic": "HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)",
                "options": [
                    {"key": "A", "text": "To eliminate transport-layer TCP Head-of-Line blocking (a single dropped packet in TCP stalls all multiplexed streams) and provide 0-RTT connection establishment"},
                    {"key": "B", "text": "Because UDP packets are automatically encrypted by hardware NICs"},
                    {"key": "C", "text": "To remove the need for IP addressing"},
                    {"key": "D", "text": "Because TCP is deprecated by IETF"}
                ],
                "correct_option": "A",
                "explanation": "In HTTP/2 over TCP, packet loss stalls the entire connection buffer. QUIC streams are independent; packet loss in stream A does not stall stream B."
            }
        ],
        "Hard": [
            {
                "question_text": "How does Border Gateway Protocol (BGP) prevent routing loops across autonomous systems (AS) on the global Internet?",
                "topic": "Routing Protocols (BGP, OSPF, RIP)",
                "options": [
                    {"key": "A", "text": "It is a Path Vector protocol that inspects the AS-PATH attribute; if a router sees its own Autonomous System number in the advertised path, it discards the route"},
                    {"key": "B", "text": "It uses Dijkstra's Shortest Path First algorithm across all Internet routers"},
                    {"key": "C", "text": "It enforces a maximum hop count of 15 like RIP"},
                    {"key": "D", "text": "It broadcasts heartbeat ICMP ping packets to all root nameservers"}
                ],
                "correct_option": "A",
                "explanation": "BGP's AS-PATH attribute acts as a loop-prevention mechanism and metric: any BGP router detecting its own AS number in the inbound path immediately rejects the route."
            }
        ]
    }
}

EXTRA_TEXT_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Java Developer": {
        "Easy": [
            {
                "question_text": "Explain the difference between `==` and the `.equals()` method in Java. When should each be used?",
                "topic": "Core Java OOP & Polymorphism",
                "model_answer": "In Java:\n- `==` is a reference equality operator when applied to objects; it checks whether both references point to the exact same memory address on the heap. For primitives, it checks numerical value equality.\n- `.equals()` is a method declared in `java.lang.Object` intended for logical value equality (content equality).\n\nWhen comparing objects (such as Strings, custom entities, or collections), always use `.equals()` (or `Objects.equals(a, b)` to safely handle nulls)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain how Java handles String immutability and describe how the String Constant Pool optimizes memory usage.",
                "topic": "Core Java OOP & Polymorphism",
                "model_answer": "In Java, `String` instances are immutable; their internal character/byte arrays cannot be modified after instantiation.\n\n- **String Constant Pool**: Located in the heap (Metaspace/Heap depending on JVM version), this pool stores unique string literal values. When a literal is declared (e.g., `String s = \"test\"`), the JVM checks the pool and returns the cached reference if present, reducing memory footprint.\n- **Security & Concurrency**: Immutability makes Strings inherently thread-safe and safe for use as HashMap keys and sensitive parameters (e.g. database credentials, network URLs)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain how the Java ThreadPoolExecutor works. Detail the role of `corePoolSize`, `maximumPoolSize`, `workQueue`, and `RejectedExecutionHandler`.",
                "topic": "Java Concurrency & Multi-threading",
                "model_answer": "1. **Submission Flow**: When a task is submitted, if fewer than `corePoolSize` threads are active, a new core thread is spawned.\n2. **Queueing**: If core threads are busy, the task is enqueued into `workQueue` (e.g. LinkedBlockingQueue).\n3. **Max Pool Expansion**: If the workQueue is full, the pool spawns additional worker threads up to `maximumPoolSize`.\n4. **Rejection Policy**: If `maximumPoolSize` threads are busy and the queue is full, the `RejectedExecutionHandler` handles the task (e.g. `AbortPolicy` throws an exception, `CallerRunsPolicy` executes in calling thread)."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain the difference between Optimistic Locking and Pessimistic Locking in JPA/Hibernate and describe when to use each.",
                "topic": "Hibernate & JPA Persistence",
                "model_answer": "- **Optimistic Locking**: Assumes write collisions are rare. Uses a `@Version` column (timestamp or number). On update, Hibernate asserts `WHERE id = ? AND version = ?`. If another transaction incremented the version, an `OptimisticLockException` is thrown. Best for high-concurrency read-heavy applications.\n- **Pessimistic Locking**: Assumes collisions will occur. Acquires explicit database row locks (e.g. `SELECT ... FOR UPDATE` via `LockModeType.PESSIMISTIC_WRITE`). Other transactions wait or time out. Best for critical financial balances or inventory decrement operations."
            }
        ],
        "Hard": [
            {
                "question_text": "Describe the internal architecture and garbage collection phases of the ZGC (Z Garbage Collector) in modern Java.",
                "topic": "JVM Memory Model & Garbage Collection",
                "model_answer": "ZGC is a scalable, low-latency concurrent garbage collector designed for heaps ranging from megabytes to multiple terabytes with pause times under 1 millisecond.\n\n- **Colored Pointers**: ZGC embeds metadata flags (Marked0, Marked1, Remapped) directly within unused reference pointer bits.\n- **Load Barriers**: Intercepts object dereferences during execution. If an object was relocated, the load barrier updates the reference on the fly (self-healing pointers).\n- **Concurrent Phases**: Almost all phases (Marking, Relocation, Reference Processing) run concurrently with application threads, eliminating Stop-The-World pauses."
            }
        ]
    },
    "Frontend Developer": {
        "Easy": [
            {
                "question_text": "Explain the difference between `let`, `const`, and `var` in JavaScript regarding scope, hoisting, and re-assignment.",
                "topic": "JavaScript ES6+ & DOM Manipulation",
                "model_answer": "- **var**: Function-scoped (or global), hoisted to top of scope initialized to `undefined`, and permits re-declaration.\n- **let**: Block-scoped (within `{}`), hoisted but resides in the Temporal Dead Zone (TDZ) until evaluation, permits re-assignment but not re-declaration in the same scope.\n- **const**: Block-scoped and subject to TDZ. Must be initialized upon declaration and cannot be re-assigned (though properties of objects assigned to `const` can still be mutated)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the concept of CSS specificity and how the browser determines which rule applies when conflicts occur.",
                "topic": "CSS Architecture, Flexbox & Grid",
                "model_answer": "CSS Specificity is calculated as a hierarchy tuple (Inline, IDs, Classes/Attributes/Pseudo-classes, Elements/Pseudo-elements):\n1. `!important` overrides normal specificity calculations.\n2. Inline styles (`style=\"...\"`): Weight 1-0-0-0.\n3. IDs (`#header`): Weight 0-1-0-0.\n4. Classes, attributes, pseudo-classes (`.btn`, `[type=\"text\"]`, `:hover`): Weight 0-0-1-0.\n5. Elements and pseudo-elements (`div`, `p`, `::before`): Weight 0-0-0-1.\nWhen two conflicting rules have identical specificity, the rule declared later in the stylesheet wins."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain how the React Reconciliation algorithm (Fiber) works and how it achieves 60fps UI responsiveness.",
                "topic": "React Hooks & Component Lifecycle",
                "model_answer": "React Fiber is a complete rewrite of the reconciliation engine from a stack-based synchronous recursion to an interruptible virtual stack frame architecture.\n\n- **Fiber Nodes**: Each component instance maps to a Fiber node holding state, props, and child/sibling pointers.\n- **Two Phases**:\n  1. **Render/Reconciliation Phase**: Asynchronous and interruptible. React computes the diff between current and work-in-progress Fiber trees, breaking work into slices yielded via cooperative scheduling (`requestIdleCallback` or MessageChannel).\n  2. **Commit Phase**: Synchronous and uninterrupted. Flushes DOM mutations and runs layout effects."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain how Cross-Site Request Forgery (CSRF) attacks operate and describe modern defensive mechanisms including SameSite cookies and anti-CSRF tokens.",
                "topic": "Frontend Security (XSS, CSRF & CSP)",
                "model_answer": "CSRF exploits the browser's default behavior of automatically attaching stored session cookies to cross-origin requests initiated by malicious third-party sites.\n\n- **Defenses**:\n  1. **SameSite Cookie Attribute**: Setting `SameSite=Lax` or `Strict` prevents the browser from sending cookies on cross-site subresource requests.\n  2. **Anti-CSRF Tokens**: A cryptographically random token tied to the user session, sent in an HTTP request header (e.g. `X-CSRF-Token`) that third-party sites cannot read due to the Same-Origin Policy.\n  3. **Custom Headers & Origin Verification**: Validating `Origin` and `Referer` headers."
            }
        ],
        "Hard": [
            {
                "question_text": "Explain Micro-Frontend architectures. Compare module federation (Webpack 5) versus iframe and Web Components integration strategies.",
                "topic": "Critical Rendering Path & Bundle Splitting",
                "model_answer": "Micro-frontends decompose monolithic SPAs into independently deployable frontend applications.\n\n- **Module Federation**: Allows applications to dynamically load remote JavaScript chunks at runtime while sharing common dependencies (like React or UI design systems) as singletons, avoiding duplicate bundle overhead.\n- **iframes**: Maximum sandbox isolation (CSS, JS, DOM cannot conflict), but suffers from rigid responsive layouts, communication friction (`postMessage`), and heavy memory usage.\n- **Web Components**: Provides framework-agnostic component encapsulation via Shadow DOM, ideal for cross-framework design systems."
            }
        ]
    },
    "Backend Developer": {
        "Easy": [
            {
                "question_text": "Explain the difference between symmetric and asymmetric encryption, and give a typical backend use case for each.",
                "topic": "Authentication, JWT Security & Refresh Rotation",
                "model_answer": "- **Symmetric Encryption (AES)**: Uses the exact same secret key for both encryption and decryption. Very fast computationally. Ideal for encrypting data at rest (e.g. database columns, backups, disk volumes).\n- **Asymmetric Encryption (RSA, ECC)**: Uses a mathematically paired public key (for encryption or signature verification) and private key (for decryption or signing). Slower. Ideal for TLS handshakes, digital signatures, and JWT asymmetric verification (RS256)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "What is database normalization? Explain 1NF, 2NF, and 3NF in relational schema design.",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "model_answer": "Normalization organizes database columns and tables to eliminate data redundancy and prevent update/delete anomalies.\n- **1NF**: Atomic values (no repeating groups or comma-separated lists), unique primary key.\n- **2NF**: Meets 1NF, and every non-key column is fully functionally dependent on the entire primary key (eliminates partial key dependencies on composite keys).\n- **3NF**: Meets 2NF, and no non-key column depends transitively on another non-key column (eliminates transitive dependencies)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain the Write-Ahead Logging (WAL) mechanism in relational database engines and how it guarantees durability (ACID).",
                "topic": "SQL Transaction Isolation Levels & ACID",
                "model_answer": "WAL ensures that no data page is written to permanent database storage until the corresponding log record describing the change has been flushed to sequential disk log storage.\n\n1. **Performance**: Appending sequentially to the WAL log file is orders of magnitude faster than random disk I/O on table pages.\n2. **Crash Recovery**: If the server crashes or loses power, the database engine inspects the WAL upon reboot, replaying committed transactions (Redo) and rolling back uncommitted changes (Undo) to restore a consistent state."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain how API gateways implement the Token Bucket rate-limiting algorithm using Redis and Lua scripting.",
                "topic": "API Rate Limiting & Token Bucket Algorithms",
                "model_answer": "In distributed microservices, rate-limiting counters in application memory fail when multiple gateway instances run in parallel.\n\n- **Redis + Lua Architecture**: An atomic Lua script runs directly on the Redis server, executing key lookups, calculating token replenishment based on `(now - last_refill_time) * refill_rate`, and checking if `current_tokens >= requested`.\n- **Atomicity**: Because Redis executes Lua scripts as a single atomic unit, race conditions between concurrent requests are prevented without distributed lock overhead."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a globally distributed database sharding strategy. Contrast range-based, hash-based, and directory-based sharding and explain how to handle resharding.",
                "topic": "Database Sharding & Read Replicas",
                "model_answer": "Sharding partitions a database horizontally across multiple physical servers.\n\n- **Hash-Based Sharding**: Applies a consistent hashing function to the shard key (e.g. `hash(user_id) % N`). Distributes data evenly and avoids hotspots, but cross-shard range queries are expensive.\n- **Range-Based Sharding**: Partitions by contiguous key ranges (e.g. timestamps or alphabetical). Efficient for range queries, but creates write hotspots on recent ranges.\n- **Resharding with Minimal Disruption**: Consistent hashing with virtual nodes minimizes data migration when adding shards. Dual-writing with backfill jobs allows online zero-downtime shard splitting."
            }
        ]
    },
    "Data Analyst": {
        "Easy": [
            {
                "question_text": "Explain the difference between categorical, ordinal, and continuous numerical data. Give an example of each.",
                "topic": "Data Cleaning & Missing Value Imputation",
                "model_answer": "- **Categorical (Nominal)**: Qualitative categories with no intrinsic mathematical order (e.g., Blood type: A, B, AB, O; Country of residence).\n- **Ordinal**: Categorical data with a clear logical order or ranking, but unequal or unquantified intervals between ranks (e.g., Customer satisfaction rating: Poor, Fair, Good, Excellent; Education level).\n- **Continuous Numerical**: Quantitative numerical measurements that can take any value within a continuum (e.g., Revenue: $1,250.75; Temperature; Customer session duration)."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain how data analysts handle missing values (NaNs) in tabular datasets. Compare deletion vs mean/median imputation vs forward-fill.",
                "topic": "Data Cleaning & Missing Value Imputation",
                "model_answer": "- **Listwise Deletion**: Drops rows with missing values. Fast, but risks losing statistical power and introducing survivorship bias if data is not Missing Completely At Random (MCAR).\n- **Mean/Median Imputation**: Replaces missing values with central tendency. Mean is sensitive to outliers; median is preferred for skewed distributions. Underestimates feature variance.\n- **Forward/Backward Fill**: Carries previous valid observation forward, ideal for time-series data.\n- **Model-Based Imputation (KNN/MICE)**: Estimates missing values from correlated features."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain SQL Window functions. Compare `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()` with a concrete analytical query example.",
                "topic": "SQL Window Functions & Aggregations",
                "model_answer": "Window functions perform calculations across a set of table rows related to the current row without collapsing the rows into a single group like `GROUP BY`.\n\n- `ROW_NUMBER()`: Assigns a strictly unique sequential integer (1, 2, 3, 4) regardless of ties.\n- `RANK()`: Assigns identical ranks to tied rows and leaves gaps matching the tie count (e.g. 1, 2, 2, 4).\n- `DENSE_RANK()`: Assigns identical ranks to tied rows but does not skip any ranks (e.g. 1, 2, 2, 3).\n\nExample: `SELECT employee_id, department, salary, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank FROM employees;`"
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain A/B Testing sample size determination and describe Type I (False Positive) and Type II (False Negative) errors.",
                "topic": "A/B Testing, Hypothesis Testing & P-Values",
                "model_answer": "- **Type I Error (Alpha, false positive)**: Concluding the test variant produced an improvement when there was no true effect (null hypothesis was true). Commonly capped at 5% (alpha = 0.05).\n- **Type II Error (Beta, false negative)**: Failing to detect a real statistically significant effect that truly exists (rejecting the alternative hypothesis). Statistical power is `1 - Beta`, commonly targeted at 80%.\n- **Sample Size Sizing**: Calculated based on baseline conversion rate, Minimum Detectable Effect (MDE), significance level (alpha), and statistical power (1 - beta) before launching the experiment."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a Customer Lifetime Value (LTV) and Churn predictive framework for an analytical business dashboard.",
                "topic": "Cohort Retention Analysis & Churn Modeling",
                "model_answer": "1. **LTV Formulation**: `LTV = (Average Order Value * Purchase Frequency) * Customer Lifespan` or `ARPU / Churn Rate` for subscription SaaS.\n2. **Cohort Analysis**: Segment users by acquisition month. Track month-over-month retention curves.\n3. **Churn Modeling**: Train gradient boosted classification (XGBoost/LightGBM) using behavioral features (days since last login, support tickets filed, feature adoption metrics).\n4. **Dashboard KPI Visualization**: Display LTV:CAC ratio (target > 3:1), net revenue retention (NRR > 105%), and cohort decay heatmaps."
            }
        ]
    },
    "Machine Learning Engineer": {
        "Easy": [
            {
                "question_text": "Explain the Bias-Variance tradeoff in supervised machine learning.",
                "topic": "Bias-Variance Tradeoff & Regularization (L1/L2)",
                "model_answer": "- **Bias**: Error introduced by approximating complex real-world relationships with an overly simplistic model (e.g., fitting a straight line to quadratic data). High bias leads to underfitting.\n- **Variance**: Error introduced by model sensitivity to small fluctuations and random noise in the training set. High variance leads to overfitting.\n- **Tradeoff**: As model complexity increases, bias decreases while variance increases. Optimal generalization minimizes Total Error = `Bias^2 + Variance + Irreducible Error`."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain the difference between Precision and Recall. Provide an example where high precision is critical, and an example where high recall is critical.",
                "topic": "Model Evaluation Metrics (Precision, Recall, ROC-AUC)",
                "model_answer": "- **Precision**: `TP / (TP + FP)` - Fraction of predicted positive instances that were truly positive. Critical when false positives are costly (e.g. spam filters where blocking an important email is unacceptable).\n- **Recall**: `TP / (TP + FN)` - Fraction of actual positive instances correctly identified. Critical when false negatives are dangerous (e.g. cancer detection or airport weapon screening where missing a positive case is catastrophic)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain Gradient Descent optimization. Contrast Batch Gradient Descent, Stochastic Gradient Descent (SGD), and Mini-Batch Gradient Descent.",
                "topic": "Gradient Descent & Optimization (Adam, SGD)",
                "model_answer": "- **Batch Gradient Descent**: Computes the gradient of the loss function over the entire dataset before updating weights. Stable and deterministic convergence, but slow and memory-intensive on large datasets.\n- **Stochastic Gradient Descent (SGD)**: Updates parameters after each single training sample. Very fast and escapes shallow local minima, but gradients fluctuate noisily.\n- **Mini-Batch Gradient Descent**: Computes gradients over a small batch (e.g. 32-256 samples). Balances hardware vectorization efficiency (GPU SIMD) with stable gradient convergence."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain how Gradient Boosted Decision Trees (XGBoost / LightGBM) differ conceptually from Random Forests.",
                "topic": "Ensemble Learning (Random Forest, XGBoost)",
                "model_answer": "- **Random Forest (Bagging)**: Trains deep, low-bias trees in parallel on bootstrap samples and averages predictions to reduce variance. Trees are independent.\n- **Gradient Boosting (Boosting)**: Trains shallow, weak trees sequentially. Each new tree fits the residual errors (pseudo-residuals / negative gradients of the loss function) made by the preceding ensemble.\n- **Tradeoff**: Boosting generally achieves higher accuracy on structured tabular datasets, but requires careful tuning (learning rate, shrinkage) to prevent overfitting."
            }
        ],
        "Hard": [
            {
                "question_text": "Design an enterprise real-time feature store and model inference pipeline with low latency and prevention of train-serve skew.",
                "topic": "Model Deployment & Inference Latency Optimization",
                "model_answer": "1. **Dual Storage Architecture**: Low-latency key-value store (Redis/DynamoDB) for online real-time point lookups (<10ms), and columnar warehouse (Snowflake/BigQuery) for offline historical training batches.\n2. **Point-in-Time Correctness**: As-of joins ensure training data only sees feature values available before the prediction timestamp, eliminating future data leakage.\n3. **Train-Serve Skew Prevention**: Centralized feature definitions ensure exact identical transformations are executed during both batch training and real-time inference.\n4. **Inference Serving**: Deploy ONNX/TensorRT compiled models on Triton Inference Server with dynamic batching."
            }
        ]
    },
    "Database Administrator": {
        "Easy": [
            {
                "question_text": "Explain the purpose of database indexes and describe the trade-off between read query performance and write performance.",
                "topic": "B-Tree vs Hash vs Bitmap Index Architecture",
                "model_answer": "Database indexes are auxiliary data structures (typically balanced B-Trees) that allow the query engine to locate matching rows in O(log N) operations without scanning every page on disk.\n\n- **Trade-off**: While indexes drastically accelerate `SELECT` filtering and joins, they incur write overhead during `INSERT`, `UPDATE`, and `DELETE` operations because the database must synchronously update the B-Tree structure and manage page splits."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain database transaction isolation levels defined by ANSI SQL and the concurrency anomalies each level prevents.",
                "topic": "ACID Properties & Write-Ahead Logging (WAL)",
                "model_answer": "1. **Read Uncommitted**: Prevents nothing; allows dirty reads (reading uncommitted changes from other transactions).\n2. **Read Committed**: Prevents dirty reads. Each query sees only data committed prior to query start.\n3. **Repeatable Read**: Prevents dirty reads and non-repeatable reads (re-reading a row in the same transaction returns identical data).\n4. **Serializable**: Highest level; prevents dirty reads, non-repeatable reads, and phantom reads (concurrent transactions execute with equivalent outcome to strict serial order)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain how to interpret PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` output to identify slow queries and query planner bottlenecks.",
                "topic": "Query Execution Plans & EXPLAIN ANALYZE",
                "model_answer": "- `EXPLAIN`: Shows the query planner's estimated cost and execution strategy.\n- `ANALYZE`: Actually executes the query and returns real execution time in milliseconds and actual row counts.\n- **Key Indicators**:\n  1. **Cost vs Actual Rows**: Large discrepancies between estimated rows and actual rows indicate stale table statistics (requires `ANALYZE table_name`).\n  2. **Seq Scan on Large Tables**: Indicates missing or non-selective index.\n  3. **Buffers Shared Hit vs Read**: `Shared Hit` indicates memory buffer cache hits; `Read` indicates slow physical disk I/O.\n  4. **Filter Rows Removed**: High count indicates index wasn't selective or was missing composite columns."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain Database Partitioning strategies (Range, List, Hash) and describe how Partition Pruning optimizes query execution.",
                "topic": "Table Partitioning & Sharding Techniques",
                "model_answer": "- **Range Partitioning**: Divides rows by continuous ranges (e.g. `created_at` by month/year). Ideal for time-series.\n- **List Partitioning**: Divides rows by explicit list of discrete values (e.g. `region IN ('US', 'EU')`).\n- **Hash Partitioning**: Distributes rows evenly by applying a modulus hash to a key (e.g. `hash(account_id) % 16`).\n- **Partition Pruning**: During query planning, the engine evaluates WHERE clauses against partition constraints. If a query filters on `created_at >= '2026-01-01'`, the optimizer prunes all 2025 and earlier partitions from execution."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a zero-downtime database migration architecture for schema changes on multi-billion row tables in PostgreSQL.",
                "topic": "Relational Schema Design & 3NF Normalization",
                "model_answer": "1. **Index Creation**: Always use `CREATE INDEX CONCURRENTLY` to avoid taking exclusive ShareLock on the table.\n2. **Column Additions**: Add nullable columns without defaults or with PostgreSQL 11+ constant defaults (stored in catalog metadata without rewriting heap tuples).\n3. **Column Renames/Type Changes**: Use the Expand and Contract pattern:\n   - Phase 1: Add new column.\n   - Phase 2: Dual-write to both columns via triggers or application code; backfill historical rows in small batches.\n   - Phase 3: Switch application reads to the new column.\n   - Phase 4: Drop old column and triggers."
            }
        ]
    },
    "Computer Networks": {
        "Easy": [
            {
                "question_text": "Explain the difference between a MAC address and an IP address.",
                "topic": "OSI Model vs TCP/IP Protocol Suite",
                "model_answer": "- **MAC Address (Media Access Control)**: A 48-bit physical hardware identifier burned into the Network Interface Card (NIC) at Layer 2 (Data Link). Used for direct hop-to-hop communication on the local broadcast domain.\n- **IP Address**: A 32-bit (IPv4) or 128-bit (IPv6) logical network address assigned dynamically or statically at Layer 3 (Network). Used for hierarchical routing and packet forwarding across heterogeneous networks."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain how DNS resolution works when a client requests an IP address for a domain name.",
                "topic": "DNS Resolution Architecture & Record Types",
                "model_answer": "1. Client checks local browser cache and operating system resolver cache.\n2. Queries Recursive DNS Resolver (e.g., ISP or 1.1.1.1).\n3. Resolver queries Root Nameserver (.) which points to the TLD nameserver (e.g., `.com`).\n4. Resolver queries TLD Nameserver which refers to Authoritative Nameserver for the target domain.\n5. Resolver queries Authoritative Nameserver which returns the A/AAAA record with TTL.\n6. Resolver caches response and returns the IP address to client."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain TCP Flow Control (Sliding Window) versus TCP Congestion Control.",
                "topic": "TCP 3-Way Handshake, Flow Control & Congestion Control",
                "model_answer": "- **Flow Control**: Prevents a fast sender from overwhelming a slow receiver's buffer. The receiver advertises its available buffer space (`Receive Window` - rwnd) in TCP header ACKs. The sender never sends more unacknowledged data than rwnd.\n- **Congestion Control**: Prevents the sender from overwhelming the intermediate network routers and links. Managed via Congestion Window (`cwnd`), dynamically adjusted via algorithms (Slow Start, Congestion Avoidance, Fast Retransmit) based on packet loss or latency telemetry."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain how the TLS 1.3 handshake establishes an encrypted communication channel in a single round trip (1-RTT).",
                "topic": "TLS/SSL Handshake & Symmetric/Asymmetric Encryption",
                "model_answer": "1. **ClientHello**: The client sends supported cipher suites and guesses the server's key exchange algorithm by speculatively sending its Diffie-Hellman public key share.\n2. **ServerHello**: The server chooses the cipher suite, sends its own DH key share, and immediately computes the shared master secret.\n3. **Encrypted Extensions & Finished**: The server sends its certificate and HMAC Finished block encrypted under the derived handshake key.\n4. **Application Data**: Client and server can immediately begin transmitting encrypted application data in 1-RTT (or 0-RTT on resumption)."
            }
        ],
        "Hard": [
            {
                "question_text": "Explain how Multiprotocol BGP (MP-BGP) and Segment Routing (SR-MPLS / SRv6) optimize traffic engineering in software-defined carrier backbones.",
                "topic": "Routing Protocols (BGP, OSPF, RIP)",
                "model_answer": "- **Segment Routing**: Replaces traditional LDP/RSVP-TE signaling by encoding packet forwarding paths directly into the packet header as an ordered list of instructions (Segments/SIDs).\n- **Source Routing**: Ingress routers compute the optimal path based on network telemetry (latency, bandwidth, packet loss) and append SID labels. Core routers simply inspect the top segment without maintaining per-flow state tables.\n- **SRv6**: Embeds segment IDs directly into IPv6 128-bit destination headers, enabling native software-defined routing across standard IP networks."
            }
        ]
    },
    "DevOps Engineer": {
        "Easy": [
            {
                "question_text": "Explain the difference between Continuous Integration (CI) and Continuous Delivery (CD).",
                "topic": "CI/CD Pipelines & GitHub Actions Workflows",
                "model_answer": "- **Continuous Integration (CI)**: Practice where developers frequently merge code into a shared repository. Every merge triggers automated builds, unit tests, and static lint analysis to catch bugs early.\n- **Continuous Delivery (CD)**: Automatically deploys validated build artifacts to staging or production environments, ensuring that software can be reliably released at any time at the push of a button."
            }
        ],
        "Easy to Medium": [
            {
                "question_text": "Explain how container namespaces and cgroups provide isolation in Linux Docker containers.",
                "topic": "Docker Containerization & Multi-stage Builds",
                "model_answer": "Containers are isolated user-space processes running on the shared host Linux kernel:\n- **Namespaces (What a container sees)**: Partitions kernel resources (PID isolates processes, NET isolates network interfaces and ports, MNT isolates filesystem mount points, IPC isolates inter-process communications).\n- **cgroups (How much a container can use)**: Enforces hard resource limits and quotas (CPU shares, memory limits, block I/O, network bandwidth)."
            }
        ],
        "Medium": [
            {
                "question_text": "Explain Kubernetes Service types: ClusterIP, NodePort, LoadBalancer, and Ingress.",
                "topic": "Kubernetes Pods, Deployments & DaemonSets",
                "model_answer": "- **ClusterIP**: Default internal service type. Exposes the service on a cluster-internal IP, accessible only within the Kubernetes cluster.\n- **NodePort**: Exposes the service on a static high port (30000-32767) on every node's external IP address.\n- **LoadBalancer**: Provisions a cloud-provider external load balancer (e.g. AWS NLB) routing traffic to NodePorts.\n- **Ingress**: Layer 7 reverse proxy managing host and path-based routing, SSL termination, and rate limiting to backend ClusterIP services."
            }
        ],
        "Medium to Hard": [
            {
                "question_text": "Explain the concept of Immutable Infrastructure and contrast it with traditional in-place server configuration management.",
                "topic": "Infrastructure as Code (Terraform & State Locking)",
                "model_answer": "- **Mutable (In-Place)**: Servers are patched and updated directly via SSH or scripts (Ansible/Puppet). Leads to configuration drift, snowflake servers, and irreproducible states.\n- **Immutable Infrastructure**: Servers/instances (AMIs or container images) are never modified after deployment. When updates are required, a new versioned image is baked and deployed via blue-green or rolling replacement, terminating old instances. Guarantees reproducibility and instant rollback."
            }
        ],
        "Hard": [
            {
                "question_text": "Design a multi-region zero-downtime disaster recovery architecture with RPO < 1 minute and RTO < 5 minutes on AWS.",
                "topic": "Cloud Networking (VPC, Subnets, Security Groups)",
                "model_answer": "1. **Active-Active / Warm Standby**: Deploy containerized services in primary (us-east-1) and secondary (us-west-2) regions using Amazon EKS and Terraform.\n2. **Data Layer**: Amazon Aurora Global Database with asynchronous storage replication across regions (typical storage lag < 1 second, RPO < 1 min).\n3. **Traffic Management**: AWS Route 53 latency-based routing with health check failover to redirect traffic upon primary outage.\n4. **Failover Execution**: Automated Lambda trigger executes Aurora promote-to-primary in secondary region and updates Route 53 DNS records (RTO < 5 minutes)."
            }
        ]
    }
}
