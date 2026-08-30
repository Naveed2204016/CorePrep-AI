# Stacks, Queues and Deques

## Stack
A LIFO structure supports push, pop, and peek in O(1). Applications include expression parsing, bracket matching, DFS, undo, and call-stack simulation.

## Monotonic stack
Maintain increasing or decreasing order so each element is pushed and popped at most once. Practise next greater element, daily temperatures, largest rectangle in histogram, and stock span.

## Queue and deque
A FIFO queue supports BFS and scheduling. A deque supports insertion and removal at both ends and enables O(n) sliding-window maximum with a monotonic deque. Avoid array-front deletion implementations that accidentally cost O(n).

## Design exercises
Implement a queue with stacks, a stack with queues, min stack, circular queue, and LRU cache (hash map plus doubly linked list).
