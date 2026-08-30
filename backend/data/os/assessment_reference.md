# Operating Systems Assessment Reference

## OS Architecture & System Calls
A system call is a controlled transition from user mode to kernel mode for privileged services such as file I/O, process creation, and memory mapping. An interrupt is generally asynchronous and hardware-originated, while an exception or trap is synchronous to the executing instruction. Good questions distinguish mechanism from policy and monolithic kernels from microkernels without claiming that one architecture is universally faster or safer.

## Processes
A process owns an address space and operating-system resources; its PCB records execution and scheduling state. A context switch saves one execution context and restores another, creating overhead without necessarily changing address spaces when switching threads. A zombie has terminated but retains an exit-status entry until its parent reaps it, whereas an orphan is still running after its parent exits.

## Threads & Multithreading
Threads in one process share code, heap, and operating-system resources while retaining separate stacks and register state. Concurrency means tasks can make overlapping progress; parallelism means tasks execute simultaneously on multiple processing units. Threads reduce some communication costs but introduce races, synchronization needs, and failure coupling.

## CPU Scheduling
FCFS is simple but can cause a convoy effect; SJF minimizes average waiting time when burst lengths are known or predicted. Round-robin improves responsiveness through a time quantum, but an extremely small quantum increases switching overhead and an extremely large one approaches FCFS. Waiting, turnaround, response, throughput, fairness, and deadline behavior measure different scheduling goals.

## Interprocess Communication
Pipes provide stream communication, message queues preserve message boundaries, and shared memory offers high throughput but requires explicit synchronization. Signals notify rather than carry substantial structured data, while sockets can communicate locally or across networks. Selection depends on data volume, isolation, latency, persistence, and coordination requirements.

## Synchronization
A race condition occurs when an outcome depends on uncontrolled interleaving of shared operations. Mutexes provide ownership-based mutual exclusion; semaphores represent permits and can coordinate ordering or bounded resources; condition variables let threads wait for predicates while releasing a lock. Correct solutions require mutual exclusion, progress, and bounded waiting while avoiding busy waiting where inappropriate.

## Deadlocks
Deadlock requires mutual exclusion, hold-and-wait, no preemption, and circular wait simultaneously. Prevention breaks at least one condition; avoidance admits requests only when the system remains in a safe state; detection allows deadlock and later finds cycles or unresolved waits. An unsafe state is not necessarily already deadlocked, and starvation is indefinite postponement rather than circular waiting.

## Memory Management
Logical addresses are translated to physical addresses through hardware and operating-system mappings. Paging uses fixed-size pages and frames, eliminating external fragmentation but permitting internal fragmentation; segmentation uses variable logical regions and can suffer external fragmentation. Allocation, relocation, protection, sharing, and fragmentation are separate concerns.

## Virtual Memory
Demand paging loads a page only when referenced and absent, causing a page fault handled by the operating system. Replacement algorithms such as FIFO, LRU approximations, and Clock make different cost and locality trade-offs; FIFO can exhibit Belady's anomaly. Thrashing occurs when active working sets exceed available frames and the system spends excessive time paging.

## File Systems
File systems map names and directories to metadata and stored blocks while enforcing permissions and consistency. Indexed allocation supports flexible random access, while contiguous allocation is fast but difficult to grow and linked allocation makes random access expensive. Journaling records intended metadata or data updates to improve crash recovery but is not a substitute for backups.

## I/O & Storage
Programmed I/O occupies the CPU, interrupts allow devices to signal completion, and DMA transfers blocks with limited CPU involvement. Buffering absorbs rate differences, caching retains reusable data, and spooling queues work for exclusive devices. RAID levels trade capacity, performance, and fault tolerance; RAID does not protect against deletion, corruption, or site loss.

## Protection & Security
Protection controls how subjects access resources, while security also addresses threats, authentication, integrity, confidentiality, and availability. Least privilege grants only required permissions, and isolation limits the impact of compromise. Access-control lists organize permissions by object, while capability systems represent delegated authority held by subjects.

## Virtualization
A hypervisor multiplexes hardware among virtual machines, each typically running its own kernel. Type-1 hypervisors run directly on hardware, while type-2 hypervisors run above a host operating system. Hardware-assisted virtualization reduces the need to emulate or rewrite sensitive operations, but virtualization still introduces resource contention and operational complexity.

## Containers & Namespaces
Containers share the host kernel while isolating views of processes, networks, mounts, users, and other resources through namespaces. Cgroups account for and limit CPU, memory, and I/O usage; layered images provide reusable filesystem content. Containers are generally lighter than virtual machines but do not create the same kernel boundary.

## OS Performance & Observability
CPU utilization alone does not reveal whether work is productive; run-queue length, context switches, latency, and saturation add necessary context. Memory pressure appears through paging, reclaim, faults, and working-set behavior, while I/O diagnosis needs throughput, queue depth, utilization, and latency. Effective diagnosis starts with symptoms and workload, then correlates multiple signals instead of optimizing a single metric.
