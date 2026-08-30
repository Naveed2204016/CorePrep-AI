# Trees

## Overview

A tree is a hierarchical data structure consisting of nodes connected by edges. A tree has one root node and zero or more subtrees connected via edges.

## Key Concepts

### Tree Terminology

- **Root**: Top node with no parent
- **Leaf**: Node with no children
- **Parent**: Node above another node
- **Child**: Node below another node
- **Siblings**: Nodes with same parent
- **Height**: Longest path from root to leaf
- **Depth**: Distance from root to node

### Binary Tree

- Each node has at most 2 children (left and right)

### Binary Search Tree (BST)

- Left child < Parent < Right child
- Enables efficient searching

### Time Complexity (Balanced Tree)

- **Search**: O(log n)
- **Insertion**: O(log n)
- **Deletion**: O(log n)
- **Traversal**: O(n)

### Space Complexity

- O(n) for n nodes
- O(h) for recursion call stack (h = height)

## Node Structure

```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
```

## Traversal Methods

### 1. Inorder (Left, Root, Right)

- For BST, gives sorted order
- ```python
  def inorder(node):
      if node:
          inorder(node.left)
          process(node.val)
          inorder(node.right)
  ```

### 2. Preorder (Root, Left, Right)

- Used for copying tree
- ```python
  def preorder(node):
      if node:
          process(node.val)
          preorder(node.left)
          preorder(node.right)
  ```

### 3. Postorder (Left, Right, Root)

- Used for deleting tree
- ```python
  def postorder(node):
      if node:
          postorder(node.left)
          postorder(node.right)
          process(node.val)
  ```

### 4. Level Order (BFS)

- Uses queue
- Process level by level

## Common Problems

- Validate BST
- Lowest Common Ancestor
- Maximum Path Sum
- Serialize/Deserialize Tree
- Vertical Order Traversal
- Path Sum
- Balanced Binary Tree

## Special Trees

1. **AVL Tree** - Balanced, height diff ≤ 1
2. **Red-Black Tree** - Balanced, color-based rules
3. **Heap** - Complete binary tree with heap property
4. **Trie** - For string search
5. **Segment Tree** - For range queries

## Balanced vs Unbalanced

- **Balanced**: O(log n) operations, good for production
- **Unbalanced**: Can degrade to O(n), avoid in practice

## Interview Tips

- Draw the tree structure
- Practice different traversals
- Handle null cases carefully
- Consider recursive vs iterative approaches
- Understand BST property implications
