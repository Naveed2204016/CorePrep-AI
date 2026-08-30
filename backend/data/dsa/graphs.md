# Graphs and Graph Algorithms

## Representation
Use adjacency lists for sparse graphs and matrices for dense graphs or constant-time edge checks. Distinguish directed/undirected and weighted/unweighted graphs. Traversal is O(V + E) with adjacency lists.

## BFS and DFS
BFS uses a queue and finds shortest paths in unweighted graphs. DFS uses recursion or an explicit stack and supports components, cycle detection, and ordering. Mark visited at the correct time and handle disconnected graphs.

## Directed acyclic graphs
Topological ordering uses indegrees (Kahn's BFS) or DFS finish times. It exists only for a DAG. Applications include course scheduling and dependency resolution.

## Union-find
Disjoint-set union with path compression and union by rank/size has near-constant amortized operations. Use it for connectivity, redundant edges, and Kruskal's minimum spanning tree.

## Weighted algorithms
Dijkstra handles nonnegative edge weights. Bellman-Ford supports negative edges and detects reachable negative cycles. Floyd-Warshall computes all-pairs paths in O(V^3). Prim and Kruskal compute minimum spanning trees for connected, weighted, undirected graphs.

## Grid graphs
Treat cells as vertices for islands, flood fill, multi-source BFS, shortest path, and boundary traversal. Be explicit about directions, bounds, and mutation vs visited storage.
