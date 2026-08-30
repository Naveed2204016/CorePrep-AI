# Arrays

## Overview

Arrays are one of the most fundamental data structures in computer science. An array is a collection of elements of the same data type stored in contiguous memory locations.

## Key Concepts

### Time Complexity

- **Access**: O(1) - Direct access using index
- **Search**: O(n) - Linear search, O(log n) with binary search (sorted)
- **Insertion**: O(n) - Due to shifting elements
- **Deletion**: O(n) - Due to shifting elements

### Space Complexity

- O(n) for storing n elements

## Common Operations

### 1. Traversal

Visiting each element of the array:

```
for i in range(len(array)):
    process(array[i])
```

### 2. Insertion

- At beginning: O(n)
- At end: O(1) amortized (dynamic arrays)
- At middle: O(n)

### 3. Deletion

- From beginning: O(n)
- From end: O(1)
- From middle: O(n)

## Common Problems

- Two Sum
- Rotate Array
- Find Maximum Subarray
- Merge Sorted Arrays
- Remove Duplicates
- Stock Buy and Sell

## Variations

1. **1D Arrays** - Single row
2. **2D Arrays** - Matrix
3. **Dynamic Arrays** - Resizable (ArrayList, Vector)
4. **Sorted Arrays** - Ordered elements
5. **Sparse Arrays** - Most elements are zero/null

## Best Practices

- Use arrays when you need fast random access (O(1))
- Use arrays for fixed-size collections
- Be aware of memory layout - contiguous storage is cache-friendly
- Consider using dynamic arrays if size is unknown

## Interview Tips

- Always clarify constraints (size limits, duplicate handling)
- Discuss trade-offs: time vs space complexity
- Consider edge cases: empty array, single element, duplicates
- Explain your approach before coding
