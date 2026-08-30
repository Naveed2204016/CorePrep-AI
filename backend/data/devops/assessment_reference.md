# DevOps Assessment Reference

## Linux Fundamentals
Permissions distinguish owner, group, and others; processes have states, signals, descriptors, and resource limits. Load average is runnable or uninterruptible demand, not CPU percentage.
## Shell Scripting
Quote expansions to avoid splitting and globbing, check exit status, and make destructive operations explicit. Pipes normally report the last command unless stricter behavior is configured.
## Git & Collaboration
Commits are immutable snapshots linked in a graph; branches are movable references. Shared-history changes favor revert over destructive reset.
## Networking & DNS
Troubleshoot link, address, route, DNS, transport, TLS, then application. DNS maps names but does not prove the destination service is reachable or healthy.
## Docker & Containers
Containers are isolated processes sharing the host kernel; images are immutable layered templates. Volumes persist data independently of a container writable layer.
## Container Images & Registries
Layer ordering affects cache reuse and size; tags can move while digests identify exact content. Scanning finds known risk but does not prove an image secure.
## Kubernetes
Deployments manage replica sets and pods; Services provide stable discovery; readiness controls traffic and liveness triggers restart. ConfigMaps are not secret storage.
## Infrastructure as Code
Declarative plans compare desired and known state. State contains mappings and often sensitive values, so locking, remote storage, review, and drift handling matter.
## Configuration Management
Idempotent tasks converge systems toward desired state. Inventories, variables, templates, handlers, and secret controls separate intent from machine-specific details.
## Continuous Integration
CI integrates small changes with automated build, test, and quality feedback. Fast deterministic pipelines and immutable artifacts reduce delayed integration risk.
## Continuous Delivery & Deployment
Delivery keeps releases deployable and may retain approval; deployment automatically releases qualifying changes. Blue-green, canary, flags, and rollback manage different risks.
## Cloud Fundamentals
Regions contain isolated availability zones; identity and network policy define access boundaries. Managed services trade control for reduced operational responsibility.
## Monitoring, Logging & Tracing
Metrics show trends, logs record events, and traces connect requests. Alerts should target actionable symptoms and SLO burn rather than every internal anomaly.
## DevSecOps
Security shifts throughout design, code, build, artifact, deployment, and runtime. Least privilege, signed provenance, scanning, policy, and secret rotation reduce supply-chain risk.
## SRE & Incident Response
SLIs measure service behavior, SLOs set objectives, and error budgets guide risk. Incidents need clear command, communication, mitigation, evidence, and blameless corrective learning.
