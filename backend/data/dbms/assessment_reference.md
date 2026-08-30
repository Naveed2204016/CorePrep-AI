# DBMS Assessment Reference

## Database Fundamentals
A schema describes structure while an instance is current data. Logical and physical data independence allow changes at one level without forcing changes above it.
## ER Modeling
Cardinality states how many entities may relate; participation states whether involvement is mandatory. Weak entities depend on owner identity and an identifying relationship.
## Relational Model & Algebra
Selection filters rows, projection chooses columns, and joins combine related tuples. Relational algebra is procedural foundation; SQL includes bags, nulls, and declarative optimization.
## SQL Fundamentals
WHERE filters before grouping and HAVING filters groups. Null uses three-valued logic, so equality with null is not a valid null test.
## Joins & Subqueries
Inner joins retain matches; outer joins preserve unmatched rows from designated sides. Correlated subqueries execute conceptually per outer row, though optimizers may transform them.
## Keys & Constraints
Candidate keys uniquely identify tuples minimally; one becomes primary. Foreign keys enforce referential integrity but do not automatically imply an efficient supporting index everywhere.
## Normalization
2NF removes partial dependency on composite keys, 3NF removes problematic transitive dependencies, and BCNF requires every determinant to be a superkey. Decomposition should preserve data and preferably dependencies.
## Indexes
B-trees support equality and ordered ranges; composite indexes follow leading-column structure. Indexes accelerate reads at storage and write-maintenance cost and do not help every low-selectivity query.
## Transactions & ACID
Atomicity is all-or-nothing, consistency preserves defined rules, isolation controls concurrent visibility, and durability survives committed failures. ACID does not mean every distributed read is immediately consistent.
## Concurrency Control
Serializability matches some serial outcome; MVCC maintains versions to reduce read-write blocking. Locks, timestamps, and optimistic validation make different contention trade-offs.
## Isolation & Deadlocks
Isolation levels permit different anomalies. Deadlock is a wait cycle; prevention, timeout, detection, and victim rollback differ from starvation handling.
## Storage & File Organization
Pages are common I/O units and buffer pools cache them. Heap files favor insertion, sorted files favor ordered access, and record layout affects scans and updates.
## Query Processing & Optimization
Plans choose scans, join order, and join algorithms using estimated cardinalities and costs. Bad statistics can cause poor plans even when SQL is logically correct.
## Replication & Partitioning
Replication copies data for availability or reads; partitioning divides data. Shard-key choice determines balance, locality, hotspots, and cross-shard cost.
## Database Security
Use parameterized queries, least privilege, encryption, auditing, and protected backups. Escaping alone is not a universal substitute for bound parameters.
