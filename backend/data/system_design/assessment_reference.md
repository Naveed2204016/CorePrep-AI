# System Design Assessment Reference

## Requirements & Capacity Estimation
Separate functional behavior from latency, scale, availability, durability, consistency, security, and cost. Estimates need explicit assumptions and orders of magnitude, not false precision.
## APIs & Communication Protocols
REST emphasizes resources, RPC procedures, GraphQL client-selected graphs, and WebSockets persistent bidirectional channels. Synchronous simplicity trades against temporal coupling.
## Load Balancing
Load balancers use health checks and distribution policies at transport or application layers. Sticky sessions can simplify state but reduce flexibility and balance.
## Caching
Caches trade freshness and complexity for latency and load reduction. TTL, eviction, invalidation, cache-aside, write-through, and stampede control address different failure modes.
## Data Modeling
Model from access patterns and invariants, not only entities. Denormalization improves selected reads while increasing duplication and consistency work.
## SQL vs NoSQL
Storage choice follows queries, transactions, scale, schema evolution, and operational maturity. NoSQL does not mean no schema or automatic unlimited scalability.
## Replication
Synchronous replication improves acknowledged durability at latency cost; asynchronous replication risks lag and acknowledged-data loss on failure. Failover needs detection and authority coordination.
## Partitioning & Sharding
Good shard keys distribute load and preserve locality. Resharding, hotspots, global constraints, and cross-shard transactions are central trade-offs.
## Message Queues & Event Streaming
Queues distribute work; logs support ordered retention and replay. At-least-once delivery requires idempotent consumers because duplicates are expected.
## Consistency & CAP
CAP concerns behavior during network partitions, not a permanent choice of only two properties. Consistency models define which writes reads may observe.
## Availability & Fault Tolerance
Timeouts bound waiting, retries need backoff and budgets, circuit breakers stop repeated doomed calls, and bulkheads contain resource failure. Redundancy without independent failure domains is weak.
## CDNs & Object Storage
CDNs serve cached content near users; object stores provide durable key-based blobs. Cache invalidation and signed access require explicit design.
## Observability
Logs describe events, metrics aggregate numeric behavior, and traces connect distributed operations. Alerts should reflect actionable user impact and SLO risk.
## System Security
Authentication establishes identity and authorization controls action. Threat modeling, encryption, secrets management, validation, and rate limits belong in the design, not as afterthoughts.
## Architecture Trade-offs
Strong answers identify bottlenecks, single points of failure, data guarantees, evolution paths, and cost. More components are not automatically a better design.
