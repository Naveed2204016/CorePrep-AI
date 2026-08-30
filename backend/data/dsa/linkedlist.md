# Linked Lists

## Overview

A linked list is a linear data structure where elements (nodes) are stored non-contiguously. Each node contains data and a reference (link) to the next node.

## Key Concepts

### Types of Linked Lists

1. **Singly Linked List** - Each node points to the next node only
2. **Doubly Linked List** - Each node points to both next and previous nodes
3. **Circular Linked List** - Last node points back to the first node

### Time Complexity

- **Access**: O(n) - Must traverse from head
- **Search**: O(n) - Linear search required
- **Insertion**: O(1) - Once position is found (O(n) to find)
- **Deletion**: O(1) - Once position is found (O(n) to find)

### Space Complexity

- O(n) for storing n elements

## Node Structure

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Singly
        self.prev = None  # Doubly
```

## Common Operations

### 1. Traversal

```python
current = head
while current:
    process(current.data)
    current = current.next
```

### 2. Insertion

- At beginning: O(1)
- At end: O(n) for singly, O(1) for doubly
- At position: O(n) to find, O(1) to insert

### 3. Deletion

- Remove head: O(1)
- Remove middle: O(n)
- Remove end: O(n)

## Common Problems

- Reverse Linked List
- Detect Cycle
- Find Middle Element
- Merge Two Sorted Lists
- Remove Nth Node from End
- Palindrome Linked List

## Advantages

- Dynamic size allocation
- Efficient insertion/deletion at known position
- No wasted memory (for sparse data)

## Disadvantages

- No random access - O(n) to access element
- Extra memory for storing references
- Cache-unfriendly (non-contiguous memory)

## When to Use

- When you need frequent insertions/deletions
- When size is unknown and varies significantly
- When you don't need random access

## Interview Tips

- Always handle null/empty cases
- Use two-pointer technique for cycle detection
- Use fast and slow pointers for middle element
- Draw diagrams while tracing through logic
