import math
import random
import numpy as np
from email.policy import default

from ply.yacc import token

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats





        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1


        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue


        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue





        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]

def greedy_pathfinder(starting_row, edges):
    path = []
    visited = set()
    path.append(starting_row)
    visited.add(starting_row)

    while len(visited) < len(edges):

        candidates = [(weight, index) for index, weight in enumerate(edges[starting_row]) if
                      index not in visited and weight != float('inf')]

        if not candidates:
            return None

        weight, next_row = min(candidates)
        visited.add(next_row)
        path.append(next_row)
        starting_row = next_row

    return path

def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    cost = float('inf')
    tour = None

    i = 0
    while i < len(edges):
        if timer.time_out():
            return stats


        potential_tour = greedy_pathfinder(i, edges)
        if potential_tour is None:
            i += 1
            continue
        else:

            best_tour = potential_tour
            best_cost = score_tour(best_tour, edges)
            if best_cost < cost:
                tour = best_tour
                cost = best_cost
            i += 1

    stats.append(SolutionStats(
        tour=tour,
        score=cost,
        time=timer.time(),
        max_queue_size=1,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    return stats


def dfs_alg(start_node, visited, edges, current_cost, path, all_paths):
    current_node = start_node
    path.append(current_node)

    if all(visited):
        total_cost = current_cost + edges[current_node][path[0]]
        all_paths.append((total_cost, path[:]))
        path.pop()
        return

    for next_city in range(len(edges)):
        if not visited[next_city]:
            visited[next_city] = True
            dfs_alg(next_city, visited, edges, current_cost + edges[current_node][next_city], path, all_paths)
            visited[next_city] = False

    path.pop()

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    start_node = 0
    visited = [False] * len(edges)
    visited[start_node] = True

    all_paths = []
    dfs_alg(start_node, visited, edges, 0, [], all_paths)

    min_cost, min_cost_path = min(all_paths, key=lambda x: x[0])

    stats.append(SolutionStats(
        tour=min_cost_path,
        score=min_cost,
        time=timer.time(),
        max_queue_size=1,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))

    return stats


def reduce_matrix(edges):
    """Creates a reduced cost matrix from the given cost matrix (edges)."""
    n = len(edges)
    reduced_matrix = [[0] * n for _ in range(n)]

    # Row reduction
    for i in range(n):
        min_row_value = min(edges[i])
        for j in range(n):
            reduced_matrix[i][j] = edges[i][j] - min_row_value

    # Precompute the minimum value for each column
    min_col_values = [min(reduced_matrix[i][j] for i in range(n)) for j in range(n)]

    # Column reduction
    for j in range(n):
        for i in range(n):
            reduced_matrix[i][j] -= min_col_values[j]

    return reduced_matrix

def calculate_lower_bound(n, visited, edges):
    reduced_cost_matrix = reduce_matrix(edges)

    cost = 0
    for node in range(n):
        if not visited[node]:
            # Find the minimum reduced cost among unvisited neighbors
            min_cost = float('inf')
            for neighbor in range(n):
                if not visited[neighbor] and neighbor != node:
                    min_cost = min(min_cost, reduced_cost_matrix[node][neighbor])
            cost += min_cost if min_cost != float('inf') else 0
    return cost

def dfs_redone(start_node, current_node, current_cost, path, visited, edges, best_cost, best_path, timer,
               n_nodes_expanded, n_nodes_pruned, tolerance=0.01):
    if timer.time_out():
        return

    n = len(edges)

    # Base case: if the path includes all nodes, close the loop and check the cost
    if len(path) == n:
        total_cost = current_cost + edges[current_node][path[0]]
        if total_cost < best_cost[0]:
            best_cost[0] = total_cost
            best_path[0] = path.copy()  # Make sure to store a copy of the path
        return

    # Calculate lower bound once at the start of the recursion
    lower_bound = calculate_lower_bound(n, visited, edges)

    # Explore all unvisited nodes
    for next_node in range(n):
        if not visited[next_node]:
            cost_to_next = edges[current_node][next_node]
            estimated_total = current_cost + cost_to_next + lower_bound

            # Prune if the estimated cost is too high
            if estimated_total + tolerance < best_cost[0]:
                visited[next_node] = True
                path.append(next_node)
                n_nodes_expanded[0] += 1
                dfs_redone(start_node, next_node, current_cost + cost_to_next, path, visited, edges, best_cost,
                           best_path, timer, n_nodes_expanded, n_nodes_pruned, tolerance)
                path.pop()  # Backtrack
                visited[next_node] = False
            else:
                n_nodes_pruned[0] += 1


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n = len(edges)
    visited = [False] * n
    greedy_result = greedy_tour(edges, timer)

    # Initialize the best cost and path with the greedy result
    best_cost = [greedy_result[0].score]
    best_path = [greedy_result[0].tour]
    n_nodes_expanded = [0]
    n_nodes_pruned = [0]
    cut_tree = CutTree(n)

    visited[0] = True
    dfs_redone(0, 0, 0, [0], visited, edges, best_cost, best_path, timer, n_nodes_expanded, n_nodes_pruned)

    stats.append(SolutionStats(
        tour=best_path[0],
        score=best_cost[0],
        time=timer.time(),
        max_queue_size=1,
        n_nodes_expanded=n_nodes_expanded[0],
        n_nodes_pruned=n_nodes_pruned[0],
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))

    return stats


def mst(remaining_nodes, edges):
    # Use Prim's or Kruskal's algorithm to compute the MST of remaining nodes
    n = len(edges)
    mst_cost = 0
    visited = [False] * n
    min_edge = [float('inf')] * n
    min_edge[remaining_nodes[0]] = 0
    for _ in remaining_nodes:
        u = min((v for v in remaining_nodes if not visited[v]), key=lambda v: min_edge[v])
        visited[u] = True
        mst_cost += min_edge[u]
        for v in remaining_nodes:
            if not visited[v] and edges[u][v] < min_edge[v]:
                min_edge[v] = edges[u][v]
    return mst_cost


def two_opt(tour, edges):
    best_tour = tour
    best_cost = score_tour(tour, edges)
    for i in range(len(tour) - 1):
        for j in range(i + 1, len(tour)):
            new_tour = best_tour[:i] + best_tour[i:j+1][::-1] + best_tour[j+1:]
            new_cost = score_tour(new_tour, edges)
            if new_cost < best_cost:
                best_tour, best_cost = new_tour, new_cost
    return best_tour


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n = len(edges)

    # Initialize with greedy result
    greedy_result = greedy_tour(edges, timer)
    best_cost = greedy_result[0].score
    best_path = greedy_result[0].tour

    # Apply 2-opt to improve the greedy path
    best_path = two_opt(best_path, edges)
    best_cost = score_tour(best_path, edges)

    # Initialize the queue as a list of tuples (cost, path, visited)
    pq = [(best_cost, best_path, [False] * n)]
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(n)

    while pq and not timer.time_out():
        # Sort the queue based on the cost (first element of the tuple)
        pq.sort(key=lambda x: x[0])

        # Pop the node with the lowest cost
        current_cost, path, visited = pq.pop(0)

        # Complete the cycle if all nodes are visited
        if len(path) == n:
            total_cost = current_cost + edges[path[-1]][path[0]]  # Complete the cycle
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path
            continue

        # Explore unvisited nodes
        for next_node in range(n):
            if not visited[next_node]:
                next_cost = current_cost + edges[path[-1]][next_node]
                next_visited = visited[:]
                next_visited[next_node] = True
                next_path = path + [next_node]

                # Calculate MST bound for the next path
                remaining_nodes = [i for i in range(n) if not next_visited[i]]
                lower_bound = mst(remaining_nodes, edges)
                total_estimate = next_cost + lower_bound

                # Prune if total estimate exceeds best cost
                if total_estimate < best_cost:
                    # Insert the new state into the queue keeping the list sorted
                    inserted = False
                    for i in range(len(pq)):
                        if total_estimate < pq[i][0]:
                            pq.insert(i, (total_estimate, next_path, next_visited))
                            inserted = True
                            break
                    if not inserted:
                        pq.append((total_estimate, next_path, next_visited))  # Append to the end if not inserted
                    n_nodes_expanded += 1
                else:
                    n_nodes_pruned += 1

    stats.append(SolutionStats(
        tour=best_path,
        score=best_cost,
        time=timer.time(),
        max_queue_size=len(pq),
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))

    return stats


# def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     stats = []
#     n = len(edges)
#     visited = [False] * n
#     greedy_result = greedy_tour(edges, timer)
#
#     # Initialize the best cost and path with the greedy result
#     best_cost = [greedy_result[0].score]
#     best_path = [greedy_result[0].tour]
#     n_nodes_expanded = [0]
#     n_nodes_pruned = [0]
#     cut_tree = CutTree(n)
#
#     visited[0] = True
#     dfs_redone(0, 0, 0, [0], visited, edges, best_cost, best_path, timer, n_nodes_expanded, n_nodes_pruned)
#
#     stats.append(SolutionStats(
#         tour=best_path[0],
#         score=best_cost[0],
#         time=timer.time(),
#         max_queue_size=1,
#         n_nodes_expanded=n_nodes_expanded[0],
#         n_nodes_pruned=n_nodes_pruned[0],
#         n_leaves_covered=cut_tree.n_leaves_cut(),
#         fraction_leaves_covered=cut_tree.fraction_leaves_covered()
#     ))
#
#     return stats
