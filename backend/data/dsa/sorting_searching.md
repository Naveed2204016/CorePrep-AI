# Sorting and Searching

## Sorting
Know stability, in-place behavior, and time/space trade-offs. Selection and insertion sort are O(n^2), with insertion sort useful for small or nearly sorted input. Merge sort is stable O(n log n) with O(n) auxiliary space. Quicksort averages O(n log n), can degrade to O(n^2), and is commonly in-place. Heap sort is O(n log n) and in-place but not stable. Counting sort is useful when the key range is bounded.

## Binary search
Use binary search on sorted data or any monotonic predicate. State the search invariant and choose inclusive or half-open bounds consistently. Practise exact lookup, first/last occurrence, lower bound, rotated arrays, matrix search, and binary search on the answer.

## Divide and conquer
Split into independent subproblems, solve recursively, and combine. Relate merge sort and quicksort to their recurrence and stack/memory behavior.

## Pitfalls
Overflow in midpoint calculations, infinite loops from incorrect bound updates, losing duplicates, assuming a predicate is monotonic, and confusing stable sorting with deterministic sorting.
