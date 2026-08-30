# Greedy Algorithms and Dynamic Programming

## Greedy reasoning
A greedy algorithm commits to a locally optimal choice. It requires a justification such as an exchange argument, staying-ahead argument, or invariant. Practise interval scheduling, meeting rooms, activity selection, fractional knapsack, jump game, and Huffman coding. Greedy does not solve 0/1 knapsack in general.

## Dynamic programming workflow
1. Define the state and what it means.
2. Write the recurrence or transition.
3. Identify base cases.
4. Choose a computation order.
5. Return the requested state and analyze states times work per transition.

## One-dimensional patterns
Fibonacci/stairs, house robber, coin change, decoding, longest increasing subsequence, and partition problems.

## Two-dimensional and sequence patterns
Grid paths, 0/1 knapsack, longest common subsequence, edit distance, interval DP, and palindrome DP. Start with memoization for correctness, then tabulate and optimize space only when dependencies permit.

## Common mistakes
Using an incomplete state, overwriting values still needed, wrong iteration direction in knapsack, confusing permutations with combinations, missing impossible-state sentinels, and giving complexity without counting all states and transitions.
