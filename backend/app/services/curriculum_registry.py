"""Curated focused-topic curricula used by roadmap generation and fallback plans."""

from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class TopicSpec:
    title: str
    description: str
    blog_url: str
    weight: int = 1

    def resources(self) -> list[dict[str, str]]:
        return [
            {"title": f"{self.title} Guide", "url": self.blog_url, "type": "Blog"},
            {
                "title": f"{self.title} Video Tutorial",
                "url": "https://www.youtube.com/results?search_query=" + quote_plus(f"{self.title} tutorial"),
                "type": "YouTube",
            },
        ]


def t(title: str, description: str, url: str, weight: int = 1) -> TopicSpec:
    return TopicSpec(title, description, url, weight)


CURRICULA: dict[str, list[TopicSpec]] = {
    "Object-Oriented Programming": [
        t("OOP Foundations", "Understand objects, classes, state, behavior, identity, and why object-oriented design is used.", "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/", 2),
        t("Classes & Objects", "Design cohesive classes, create objects, and distinguish instance data from behavior.", "https://docs.oracle.com/javase/tutorial/java/javaOO/classes.html", 2),
        t("Encapsulation", "Protect invariants with access control, information hiding, and intentional public APIs.", "https://www.geeksforgeeks.org/encapsulation-in-java/", 2),
        t("Abstraction & Interfaces", "Model contracts with abstract types and interfaces while hiding implementation details.", "https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html", 2),
        t("Inheritance", "Apply inheritance only for valid is-a relationships and understand its coupling trade-offs.", "https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html"),
        t("Polymorphism", "Use subtype polymorphism and dynamic dispatch to replace conditional behavior.", "https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html", 2),
        t("Composition", "Prefer composition for flexible has-a relationships and delegation-based reuse.", "https://en.wikipedia.org/wiki/Composition_over_inheritance", 2),
        t("Object Construction", "Handle constructors, initialization order, factories, immutability, and object lifecycle.", "https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html"),
        t("Method Overloading & Overriding", "Distinguish compile-time overload resolution from runtime method overriding.", "https://www.geeksforgeeks.org/difference-between-method-overloading-and-method-overriding-in-java/"),
        t("SOLID Principles", "Apply SRP, OCP, LSP, ISP, and DIP to maintainable object-oriented designs.", "https://www.baeldung.com/solid-principles", 3),
        t("Design Patterns", "Recognize creational, structural, and behavioral patterns and their trade-offs.", "https://refactoring.guru/design-patterns", 3),
        t("Exception Handling", "Design exception boundaries, preserve context, and separate recoverable from fatal failures.", "https://docs.oracle.com/javase/tutorial/essential/exceptions/"),
        t("Generics & Collections", "Use generic abstractions and choose collections by ordering, lookup, and mutation needs.", "https://docs.oracle.com/javase/tutorial/java/generics/", 2),
        t("Equality & Object Contracts", "Implement equality, hashing, comparison, and string representation consistently.", "https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html"),
        t("Object-Oriented Design", "Translate requirements into responsibilities, collaborations, testable boundaries, and class diagrams.", "https://www.geeksforgeeks.org/system-design/oops-system-design/", 3),
    ],
    "DBMS": [
        t("Database Fundamentals", "Understand database systems, schemas, instances, data independence, and DBMS architecture.", "https://www.geeksforgeeks.org/dbms/", 2),
        t("ER Modeling", "Model entities, attributes, relationships, cardinality, and participation constraints.", "https://www.geeksforgeeks.org/introduction-of-er-model/", 2),
        t("Relational Model & Algebra", "Reason with relations, tuples, selection, projection, joins, and set operations.", "https://www.geeksforgeeks.org/introduction-of-relational-algebra-in-dbms/", 2),
        t("SQL Fundamentals", "Write correct DDL, DML, filtering, grouping, aggregation, and ordering queries.", "https://www.postgresql.org/docs/current/tutorial-sql.html", 3),
        t("Joins & Subqueries", "Choose joins, correlated subqueries, CTEs, and set operations for multi-table questions.", "https://www.postgresql.org/docs/current/queries-table-expressions.html", 3),
        t("Keys & Constraints", "Use candidate, primary, foreign, unique, check, and nullability constraints.", "https://www.postgresql.org/docs/current/ddl-constraints.html", 2),
        t("Normalization", "Identify dependencies and normalize schemas through 1NF, 2NF, 3NF, and BCNF.", "https://www.geeksforgeeks.org/normal-forms-in-dbms/", 3),
        t("Indexes", "Understand B-tree and hash indexes, composite keys, selectivity, and write overhead.", "https://www.postgresql.org/docs/current/indexes.html", 3),
        t("Transactions & ACID", "Use atomicity, consistency, isolation, durability, commit, and rollback correctly.", "https://www.postgresql.org/docs/current/tutorial-transactions.html", 3),
        t("Concurrency Control", "Understand locks, timestamps, MVCC, serializability, and concurrent anomalies.", "https://www.postgresql.org/docs/current/mvcc.html", 3),
        t("Isolation & Deadlocks", "Compare isolation levels, detect anomalies, and prevent or resolve deadlocks.", "https://www.postgresql.org/docs/current/transaction-iso.html", 2),
        t("Storage & File Organization", "Understand pages, records, heap files, buffer management, and disk access costs.", "https://www.geeksforgeeks.org/file-organization-in-dbms-set-1/"),
        t("Query Processing & Optimization", "Read query plans and reason about scan, join, cardinality, and cost choices.", "https://www.postgresql.org/docs/current/using-explain.html", 3),
        t("Replication & Partitioning", "Compare replication, sharding, partitioning, availability, and consistency trade-offs.", "https://www.postgresql.org/docs/current/ddl-partitioning.html", 2),
        t("Database Security", "Apply authentication, roles, privileges, parameterization, encryption, and auditing.", "https://www.postgresql.org/docs/current/ddl-priv.html", 2),
    ],
    "Operating Systems": [
        t("OS Architecture & System Calls", "Understand kernel/user mode, interrupts, traps, services, and system-call boundaries.", "https://www.geeksforgeeks.org/operating-systems/", 2),
        t("Processes", "Model process states, PCBs, context switching, creation, termination, and zombies.", "https://www.geeksforgeeks.org/introduction-of-process-management/", 3),
        t("Threads & Multithreading", "Compare user and kernel threads, concurrency, parallelism, and threading models.", "https://www.geeksforgeeks.org/thread-in-operating-system/", 3),
        t("CPU Scheduling", "Compare FCFS, SJF, priority, round-robin, multilevel queues, and scheduling metrics.", "https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/", 3),
        t("Interprocess Communication", "Use pipes, message queues, shared memory, signals, sockets, and RPC.", "https://www.geeksforgeeks.org/inter-process-communication-ipc/", 2),
        t("Synchronization", "Reason about race conditions, critical sections, mutexes, semaphores, monitors, and atomicity.", "https://www.geeksforgeeks.org/process-synchronization-in-operating-system/", 3),
        t("Deadlocks", "Apply necessary conditions, prevention, avoidance, detection, recovery, and Banker's algorithm.", "https://www.geeksforgeeks.org/introduction-of-deadlock-in-operating-system/", 3),
        t("Memory Management", "Understand address binding, allocation, fragmentation, paging, and segmentation.", "https://www.geeksforgeeks.org/memory-management-in-operating-system/", 3),
        t("Virtual Memory", "Reason about demand paging, page faults, replacement algorithms, locality, and thrashing.", "https://www.geeksforgeeks.org/virtual-memory-in-operating-system/", 3),
        t("File Systems", "Understand files, directories, allocation, metadata, journaling, and permissions.", "https://www.geeksforgeeks.org/file-systems-in-operating-system/", 2),
        t("I/O & Storage", "Understand device controllers, interrupts, DMA, buffering, caching, disks, and RAID.", "https://www.geeksforgeeks.org/io-systems-in-operating-system/"),
        t("Protection & Security", "Apply access control, isolation, least privilege, and common OS security defenses.", "https://www.geeksforgeeks.org/system-protection-in-operating-system/", 2),
        t("Virtualization", "Compare hypervisors, virtual machines, hardware assistance, and resource isolation.", "https://www.redhat.com/en/topics/virtualization/what-is-virtualization", 2),
        t("Containers & Namespaces", "Understand process isolation with namespaces, cgroups, images, and containers.", "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/", 2),
        t("OS Performance & Observability", "Measure CPU, memory, I/O, load, contention, and diagnose resource bottlenecks.", "https://www.brendangregg.com/linuxperf.html", 2),
    ],
    "Computer Networks": [
        t("OSI & TCP/IP Models", "Map networking responsibilities across layers and understand encapsulation.", "https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/", 2),
        t("Physical & Data Link Layers", "Understand signals, framing, error detection, switching, and link delivery.", "https://www.geeksforgeeks.org/data-link-layer/"),
        t("Ethernet, MAC & VLANs", "Reason about MAC addressing, switching, collision domains, VLANs, and trunks.", "https://www.cloudflare.com/learning/network-layer/what-is-a-mac-address/", 2),
        t("IP Addressing & Subnetting", "Calculate IPv4/IPv6 addresses, prefixes, subnet ranges, and CIDR aggregation.", "https://www.cloudflare.com/learning/network-layer/what-is-my-ip-address/", 3),
        t("ARP, ICMP & NAT", "Explain local address resolution, diagnostics, translation, and packet forwarding.", "https://www.cloudflare.com/learning/network-layer/what-is-icmp/", 2),
        t("Routing", "Understand routing tables, longest-prefix matching, distance-vector, link-state, and BGP basics.", "https://www.cloudflare.com/learning/network-layer/what-is-routing/", 3),
        t("TCP", "Master connection setup, reliability, sequencing, flow control, congestion control, and teardown.", "https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/", 3),
        t("UDP", "Understand connectionless delivery, loss trade-offs, datagrams, and latency-sensitive use cases.", "https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/", 2),
        t("DNS", "Trace recursive and iterative resolution, caching, records, TTLs, and DNS security.", "https://www.cloudflare.com/learning/dns/what-is-dns/", 3),
        t("HTTP & HTTPS", "Understand methods, status codes, headers, cookies, versions, and request lifecycles.", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", 3),
        t("TLS", "Explain certificates, handshakes, key exchange, encryption, integrity, and trust chains.", "https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/", 3),
        t("Sockets & Client-Server Communication", "Use sockets, ports, connection lifecycles, multiplexing, and RPC concepts.", "https://docs.python.org/3/howto/sockets.html", 2),
        t("Firewalls & Network Security", "Apply filtering, segmentation, proxies, VPNs, IDS/IPS, and zero-trust principles.", "https://www.cloudflare.com/learning/security/what-is-a-firewall/", 2),
        t("Wireless Networks", "Understand Wi-Fi standards, channels, association, interference, and wireless security.", "https://www.cisco.com/c/en/us/products/wireless/what-is-wifi.html"),
        t("Network Troubleshooting", "Diagnose connectivity using ping, traceroute, DNS tools, packet capture, and layered reasoning.", "https://www.cloudflare.com/learning/network-layer/how-does-traceroute-work/", 2),
    ],
    "System Design": [
        t("Requirements & Capacity Estimation", "Clarify functional and nonfunctional requirements and estimate traffic, storage, and bandwidth.", "https://github.com/donnemartin/system-design-primer", 3),
        t("APIs & Communication Protocols", "Choose REST, RPC, GraphQL, WebSockets, and synchronous or asynchronous communication.", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Introduction", 2),
        t("Load Balancing", "Distribute traffic using algorithms, health checks, layers, and failover strategies.", "https://www.cloudflare.com/learning/performance/what-is-load-balancing/", 3),
        t("Caching", "Design browser, CDN, application, and database caches with invalidation and eviction policies.", "https://aws.amazon.com/caching/", 3),
        t("Data Modeling", "Choose entities, access patterns, relationships, constraints, and denormalization deliberately.", "https://www.postgresql.org/docs/current/ddl.html", 3),
        t("SQL vs NoSQL", "Select relational, document, key-value, wide-column, or graph storage by workload.", "https://aws.amazon.com/compare/the-difference-between-relational-and-non-relational-databases/", 3),
        t("Replication", "Use leader-follower, multi-leader, quorum, and failover replication patterns.", "https://www.postgresql.org/docs/current/different-replication-solutions.html", 2),
        t("Partitioning & Sharding", "Partition data, select shard keys, rebalance, and handle cross-shard operations.", "https://www.mongodb.com/docs/manual/sharding/", 3),
        t("Message Queues & Event Streaming", "Decouple services using queues, logs, delivery semantics, and idempotent consumers.", "https://aws.amazon.com/message-queue/", 3),
        t("Consistency & CAP", "Reason about consistency models, availability, partitions, quorums, and eventual consistency.", "https://www.ibm.com/think/topics/cap-theorem", 3),
        t("Availability & Fault Tolerance", "Remove single points of failure with redundancy, retries, timeouts, and circuit breakers.", "https://learn.microsoft.com/en-us/azure/architecture/framework/resiliency/overview", 3),
        t("CDNs & Object Storage", "Serve static and large objects using edge caching, blobs, signed URLs, and lifecycle rules.", "https://www.cloudflare.com/learning/cdn/what-is-a-cdn/", 2),
        t("Observability", "Design logs, metrics, traces, alerts, dashboards, and service-level objectives.", "https://opentelemetry.io/docs/concepts/observability-primer/", 2),
        t("System Security", "Apply authentication, authorization, encryption, rate limiting, secrets, and threat modeling.", "https://owasp.org/www-project-top-ten/", 3),
        t("Architecture Trade-offs", "Evaluate bottlenecks, cost, complexity, evolution, and failure modes in complete designs.", "https://github.com/donnemartin/system-design-primer", 3),
    ],
    "Frontend Development": [
        t("Semantic HTML & Accessibility", "Build meaningful document structure, forms, keyboard navigation, and accessible interfaces.", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML", 3),
        t("CSS Fundamentals & Layout", "Master cascade, specificity, box model, Flexbox, Grid, and responsive layout.", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics", 3),
        t("JavaScript Fundamentals", "Use types, scope, functions, objects, arrays, modules, and modern language features.", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", 3),
        t("TypeScript", "Apply static types, narrowing, interfaces, generics, utility types, and safe configuration.", "https://www.typescriptlang.org/docs/handbook/intro.html", 3),
        t("DOM & Events", "Query and update the DOM, handle propagation, delegation, forms, and browser events.", "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction", 2),
        t("Browser Rendering", "Understand parsing, CSSOM, layout, paint, compositing, and the critical rendering path.", "https://web.dev/articles/critical-rendering-path", 2),
        t("HTTP & Web APIs", "Use fetch, headers, status codes, cookies, CORS, JSON, and asynchronous requests.", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", 3),
        t("React Components & Hooks", "Build component trees and use state, effects, refs, context, and custom hooks correctly.", "https://react.dev/learn", 3),
        t("State Management", "Separate local, shared, server, and URL state and select appropriate state tools.", "https://react.dev/learn/managing-state", 3),
        t("Forms & Validation", "Create accessible controlled forms with client/server validation and useful error states.", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation", 2),
        t("Routing & Application Architecture", "Structure routes, layouts, data loading, boundaries, and reusable feature modules.", "https://reactrouter.com/start/framework/routing", 2),
        t("Frontend Testing", "Test behavior with unit, component, integration, accessibility, and end-to-end strategies.", "https://testing-library.com/docs/", 3),
        t("Web Performance", "Measure and improve Core Web Vitals, loading, rendering, code splitting, and caching.", "https://web.dev/learn/performance/", 3),
        t("Frontend Security", "Prevent XSS, CSRF, unsafe DOM use, dependency risk, and credential leakage.", "https://owasp.org/www-project-top-ten/", 2),
        t("Build Tools & Deployment", "Use package managers, bundlers, environment configuration, CI, and static hosting.", "https://vite.dev/guide/", 2),
    ],
    "Backend Development": [
        t("Backend & Server Fundamentals", "Understand servers, processes, concurrency, request lifecycles, and runtime choices.", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Introduction", 2),
        t("REST API Design", "Design resources, methods, status codes, pagination, filtering, versioning, and idempotency.", "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design", 3),
        t("Validation & Error Handling", "Validate boundaries and return consistent, safe, actionable error responses.", "https://fastapi.tiangolo.com/tutorial/handling-errors/", 2),
        t("Authentication & Authorization", "Implement sessions or tokens, identity flows, roles, permissions, and least privilege.", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html", 3),
        t("SQL & Database Design", "Model relational data, write queries, enforce constraints, and use transactions.", "https://www.postgresql.org/docs/current/tutorial.html", 3),
        t("ORMs & Migrations", "Use object mapping deliberately and evolve schemas safely through migrations.", "https://docs.sqlalchemy.org/en/20/tutorial/", 2),
        t("Caching", "Cache expensive data with TTLs, invalidation, eviction, and stampede protection.", "https://redis.io/docs/latest/develop/", 3),
        t("Background Jobs & Queues", "Move slow work to reliable workers with retries, idempotency, scheduling, and dead letters.", "https://docs.celeryq.dev/en/stable/getting-started/introduction.html", 2),
        t("File & Object Storage", "Handle uploads, streaming, metadata, validation, object storage, and signed access.", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
        t("Backend Testing", "Test services, APIs, databases, contracts, and failure paths with isolated fixtures.", "https://fastapi.tiangolo.com/tutorial/testing/", 3),
        t("Backend Security", "Prevent injection, broken access control, SSRF, insecure secrets, and dependency attacks.", "https://owasp.org/www-project-api-security/", 3),
        t("Logging & Observability", "Produce structured logs, metrics, traces, correlation IDs, alerts, and health checks.", "https://opentelemetry.io/docs/concepts/observability-primer/", 2),
        t("Scalability & Reliability", "Use stateless services, load balancing, timeouts, retries, and graceful degradation.", "https://learn.microsoft.com/en-us/azure/architecture/framework/resiliency/overview", 3),
        t("Containers & Deployment", "Package services, configure environments, run migrations, and deploy safely.", "https://docs.docker.com/get-started/", 2),
        t("Backend Architecture", "Apply layering, modularity, dependency inversion, event-driven design, and trade-off analysis.", "https://learn.microsoft.com/en-us/azure/architecture/guide/", 3),
    ],
    "Machine Learning": [
        t("Math & Statistics Foundations", "Review linear algebra, probability, distributions, estimation, and hypothesis testing.", "https://developers.google.com/machine-learning/crash-course/prereqs-and-prework", 3),
        t("Data Preparation", "Clean missing values, encode categories, scale features, split data, and prevent leakage.", "https://scikit-learn.org/stable/modules/preprocessing.html", 3),
        t("EDA & Feature Engineering", "Explore distributions and relationships and create informative, stable features.", "https://scikit-learn.org/stable/modules/compose.html", 2),
        t("Linear Regression", "Understand loss, assumptions, fitting, regularization, interpretation, and diagnostics.", "https://scikit-learn.org/stable/modules/linear_model.html", 3),
        t("Classification", "Use logistic regression and probabilistic decision boundaries for classification tasks.", "https://scikit-learn.org/stable/supervised_learning.html", 3),
        t("Trees & Ensemble Models", "Train decision trees, random forests, bagging, and gradient boosting models.", "https://scikit-learn.org/stable/modules/ensemble.html", 3),
        t("Unsupervised Learning", "Apply clustering, dimensionality reduction, and anomaly detection appropriately.", "https://scikit-learn.org/stable/unsupervised_learning.html", 2),
        t("Model Evaluation", "Choose metrics, cross-validation, baselines, thresholding, and error analysis.", "https://scikit-learn.org/stable/modules/model_evaluation.html", 3),
        t("Overfitting & Regularization", "Manage bias and variance with regularization, validation, early stopping, and more data.", "https://developers.google.com/machine-learning/crash-course/overfitting/overfitting", 3),
        t("Optimization", "Understand gradient descent, learning rates, objectives, convexity, and optimization behavior.", "https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent", 2),
        t("Neural Networks", "Understand layers, activations, backpropagation, initialization, normalization, and training.", "https://developers.google.com/machine-learning/crash-course/neural-networks", 3),
        t("Natural Language Processing", "Represent text and understand embeddings, sequence models, attention, and transformers.", "https://huggingface.co/learn/nlp-course/chapter1/1", 2),
        t("Computer Vision", "Understand image representation, convolution, augmentation, classification, and detection.", "https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html", 2),
        t("ML Deployment & MLOps", "Package models, version data, serve predictions, monitor drift, and retrain safely.", "https://developers.google.com/machine-learning/managing-ml-projects", 3),
        t("Responsible ML", "Evaluate fairness, explainability, privacy, safety, and human impact.", "https://developers.google.com/machine-learning/responsible-ai", 2),
    ],
    "DevOps": [
        t("Linux Fundamentals", "Use filesystems, permissions, processes, services, packages, and resource inspection.", "https://www.redhat.com/en/topics/linux/what-is-linux", 3),
        t("Shell Scripting", "Automate repeatable operations with variables, pipes, conditions, loops, functions, and safe failure handling.", "https://www.gnu.org/software/bash/manual/bash.html", 2),
        t("Git & Collaboration", "Use commits, branches, merging, pull requests, tags, and recoverable team workflows.", "https://git-scm.com/book/en/v2", 2),
        t("Networking & DNS", "Understand IP, ports, routing, DNS, HTTP, TLS, proxies, and connectivity troubleshooting.", "https://www.cloudflare.com/learning/network-layer/what-is-a-computer-network/", 3),
        t("Docker & Containers", "Build and run isolated containers using images, volumes, networks, and Compose.", "https://docs.docker.com/get-started/", 3),
        t("Container Images & Registries", "Create small secure images, use layers and tags, scan artifacts, and manage registries.", "https://docs.docker.com/get-started/docker-concepts/building-images/", 2),
        t("Kubernetes", "Deploy and operate workloads with pods, deployments, services, configuration, and health probes.", "https://kubernetes.io/docs/tutorials/kubernetes-basics/", 3),
        t("Infrastructure as Code", "Provision reproducible infrastructure with declarative state, plans, modules, and safe changes.", "https://developer.hashicorp.com/terraform/tutorials", 3),
        t("Configuration Management", "Manage desired server state, inventories, secrets, idempotency, and environment differences.", "https://docs.ansible.com/ansible/latest/getting_started/index.html", 2),
        t("Continuous Integration", "Automate builds, tests, quality checks, artifacts, and fast feedback on every change.", "https://docs.github.com/en/actions/about-github-actions/understanding-github-actions", 3),
        t("Continuous Delivery & Deployment", "Design release pipelines, approvals, rollbacks, blue-green, canary, and progressive delivery.", "https://learn.microsoft.com/en-us/devops/deliver/what-is-continuous-delivery", 3),
        t("Cloud Fundamentals", "Understand compute, storage, networking, identity, managed services, regions, and cost trade-offs.", "https://aws.amazon.com/what-is-cloud-computing/", 2),
        t("Monitoring, Logging & Tracing", "Collect signals, build dashboards, correlate failures, and alert on actionable symptoms.", "https://opentelemetry.io/docs/concepts/observability-primer/", 3),
        t("DevSecOps", "Shift security left with least privilege, secret management, scanning, policy, and supply-chain controls.", "https://owasp.org/www-project-devsecops-guideline/", 3),
        t("SRE & Incident Response", "Use SLIs, SLOs, error budgets, on-call practices, runbooks, postmortems, and reliability engineering.", "https://sre.google/sre-book/table-of-contents/", 3),
    ],
    "Git & GitHub": [
        t("Git Foundations", "Understand distributed version control, snapshots, repositories, and the working tree.", "https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F", 2),
        t("Repository Lifecycle", "Initialize, clone, inspect, configure, and maintain local repositories.", "https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository", 2),
        t("Staging & Commits", "Create focused commits using the working tree, index, diffs, and meaningful history.", "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository", 3),
        t("Branching", "Create, switch, compare, and delete lightweight branches safely.", "https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell", 3),
        t("Merging", "Understand fast-forward and three-way merges and preserve meaningful integration history.", "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging", 3),
        t("Rebasing", "Rewrite local history safely and understand when rebasing shared work is dangerous.", "https://git-scm.com/book/en/v2/Git-Branching-Rebasing", 2),
        t("Remotes", "Fetch, pull, push, track branches, and coordinate distributed repositories.", "https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes", 3),
        t("GitHub Pull Requests", "Collaborate through forks, reviews, checks, approvals, and protected branches.", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests", 3),
        t("Conflict Resolution", "Diagnose and resolve textual conflicts during merges, rebases, and cherry-picks.", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts", 3),
        t("Undo & Recovery", "Use restore, reset, revert, reflog, and recovery techniques without losing work.", "https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified", 3),
        t("Tags & Releases", "Mark versions with tags and publish release notes and artifacts.", "https://git-scm.com/book/en/v2/Git-Basics-Tagging", 2),
        t("Stashing & Cherry-Picking", "Temporarily shelve changes and selectively apply individual commits.", "https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning", 2),
        t("Git Internals", "Understand objects, references, HEAD, packfiles, and how history is represented.", "https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain", 2),
        t("Team Workflows", "Compare feature branches, trunk-based development, GitHub Flow, and release strategies.", "https://docs.github.com/en/get-started/using-github/github-flow", 3),
        t("GitHub Actions & Security", "Automate checks and protect repositories with permissions, secrets, scanning, and dependency updates.", "https://docs.github.com/en/actions", 3),
    ],
    "Software Testing & QA": [
        t("Testing Fundamentals", "Understand quality, verification, validation, test levels, and the purpose of testing.", "https://www.geeksforgeeks.org/software-testing/", 2),
        t("Test Strategy & Planning", "Define scope, risks, environments, responsibilities, entry criteria, and exit criteria.", "https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing", 2),
        t("Test Case Design", "Derive effective cases using equivalence classes, boundaries, decision tables, and state transitions.", "https://www.geeksforgeeks.org/software-testing-techniques/", 3),
        t("Unit Testing", "Test small behaviors in isolation with deterministic setup, assertions, and maintainable doubles.", "https://martinfowler.com/bliki/UnitTest.html", 3),
        t("Integration Testing", "Verify component boundaries, databases, services, contracts, and failure interactions.", "https://martinfowler.com/bliki/IntegrationTest.html", 3),
        t("System & End-to-End Testing", "Validate complete user workflows in representative environments while controlling brittleness.", "https://playwright.dev/docs/intro", 3),
        t("Regression, Smoke & Sanity Testing", "Select efficient suites for change confidence, build health, and focused verification.", "https://www.geeksforgeeks.org/difference-between-smoke-testing-and-sanity-testing/", 2),
        t("Black-Box & White-Box Testing", "Compare behavior-based and structure-based methods including coverage and path testing.", "https://www.geeksforgeeks.org/differences-between-black-box-testing-vs-white-box-testing/", 2),
        t("API Testing", "Test status codes, schemas, authentication, validation, idempotency, errors, and contracts.", "https://learning.postman.com/docs/tests-and-scripts/write-scripts/test-scripts/", 3),
        t("UI Test Automation", "Create stable browser tests using robust locators, waits, fixtures, and page abstractions.", "https://playwright.dev/docs/best-practices", 3),
        t("Performance Testing", "Measure latency, throughput, saturation, scalability, load, stress, and endurance.", "https://grafana.com/docs/k6/latest/testing-guides/test-types/", 2),
        t("Security Testing", "Test authentication, authorization, input handling, sessions, dependencies, and common vulnerabilities.", "https://owasp.org/www-project-web-security-testing-guide/", 2),
        t("Defect Management", "Report reproducible defects, assign severity and priority, triage, retest, and close responsibly.", "https://www.atlassian.com/agile/software-development/bug-tracking"),
        t("Testing in CI/CD", "Run layered automated checks, parallelize feedback, manage test data, and block unsafe releases.", "https://docs.github.com/en/actions/automating-builds-and-tests", 3),
        t("Quality Metrics & Risk-Based Testing", "Use coverage, defect, reliability, and risk signals without optimizing misleading metrics.", "https://martinfowler.com/articles/practical-test-pyramid.html", 2),
    ],
}


ALIASES = {
    "dsa": "Data Structures & Algorithms",
    "data structures and algorithms": "Data Structures & Algorithms",
    "oop": "Object-Oriented Programming",
    "object oriented programming": "Object-Oriented Programming",
    "dbms": "DBMS",
    "os": "Operating Systems",
    "cn": "Computer Networks",
    "ml": "Machine Learning",
    "git": "Git & GitHub",
    "qa": "Software Testing & QA",
}


def canonical_subject(value: str) -> str:
    normalized = " ".join(value.lower().replace("&", "and").split())
    for subject in CURRICULA:
        if " ".join(subject.lower().replace("&", "and").split()) == normalized:
            return subject
    alias = ALIASES.get(normalized)
    if alias:
        return alias
    raise ValueError(f"Unsupported roadmap subject: {value}")


def subject_slug(subject: str) -> str:
    return {
        "Object-Oriented Programming": "oop",
        "DBMS": "dbms",
        "Operating Systems": "os",
        "Computer Networks": "computer_networks",
        "System Design": "system_design",
        "Frontend Development": "frontend",
        "Backend Development": "backend",
        "Machine Learning": "machine_learning",
        "DevOps": "devops",
        "Git & GitHub": "git_github",
        "Software Testing & QA": "software_testing",
    }.get(subject, "dsa")
