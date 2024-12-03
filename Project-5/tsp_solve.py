import math
import random
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


def dfs_shared(current_node,current_cost,path,visited,edges,
               all_paths=None,best_cost=None,best_path=None,prune=False):

    n = len(edges)

    if len(path) == n:
        if all_paths is not None:
            total_cost = current_cost + edges[current_node][path[0]]
            all_paths.append((total_cost, path[:]))
        elif current_cost < best_cost[0]:
            best_cost[0] = current_cost
            best_path[0] = path[:]
        return

    for next_node in range(n):
        if not visited[next_node]:
            cost_to_next = edges[current_node][next_node]


            if prune:
                estimated_total = current_cost + cost_to_next + calculate_lower_bound(n, visited, edges)
                if estimated_total >= best_cost[0]:
                    continue

            visited[next_node] = True
            dfs_shared(next_node,current_cost + cost_to_next,path + [next_node],visited,edges,
                all_paths,best_cost,best_path,prune
            )
            visited[next_node] = False

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    start_node = 0
    visited = [False] * len(edges)
    visited[start_node] = True

    all_paths = []
    dfs_shared(start_node, 0, [start_node], visited, edges, all_paths=all_paths)

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

def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    n = len(edges)
    visited = [False] * n
    best_cost = [float('inf')]
    best_path = [[]]

    start_node = 0
    visited[start_node] = True
    dfs_shared(
        start_node,
        0,
        [start_node],
        visited,
        edges,
        best_cost=best_cost,
        best_path=best_path,
        prune=True
    )

    stats.append(SolutionStats(
        tour=best_path[0],
        score=best_cost[0],
        time=timer.time(),
        max_queue_size=1,
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))
    return stats


# def dfs_alg(start_node, visited, edges, current_cost, path, all_paths):
#     current_node = start_node
#     path.append(current_node)
#
#     if all(visited):
#         total_cost = current_cost + edges[current_node][path[0]]
#         all_paths.append((total_cost, path[:]))
#         path.pop()
#         return
#
#     for next_city in range(len(edges)):
#         if not visited[next_city]:
#             visited[next_city] = True
#             dfs_alg(next_city, visited, edges, current_cost + edges[current_node][next_city], path, all_paths)
#             visited[next_city] = False
#
#     path.pop()
#
# def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     stats = []
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     cut_tree = CutTree(len(edges))
#
#     start_node = 0
#     visited = [False] * len(edges)
#     visited[start_node] = True
#
#     all_paths = []
#     dfs_alg(start_node, visited, edges, 0, [], all_paths)
#
#     min_cost, min_cost_path = min(all_paths, key=lambda x: x[0])
#
#     stats.append(SolutionStats(
#         tour=min_cost_path,
#         score=min_cost,
#         time=timer.time(),
#         max_queue_size=1,
#         n_nodes_expanded=n_nodes_expanded,
#         n_nodes_pruned=n_nodes_pruned,
#         n_leaves_covered=cut_tree.n_leaves_cut(),
#         fraction_leaves_covered=cut_tree.fraction_leaves_covered()
#     ))
#
#     return stats




def calculate_lower_bound(n, visited, edges):
    cost = 0
    for node in range(n):
        if not visited[node]:
            min_cost = min(
                (edges[node][neighbor] for neighbor in range(n) if neighbor != node and not visited[neighbor]),
                default=0
            )
            cost += min_cost
    return cost
#
#
# def dfs_redone(start_node, current_node, current_cost, path, visited, edges, best_cost, best_path):
#     n = len(edges)
#
#     if len(path) == n:
#         # A valid Hamiltonian path that touches all nodes
#         if current_cost < best_cost[0]:
#             best_cost[0] = current_cost
#             best_path[0] = path
#         return
#
#     for next_node in range(n):
#         if not visited[next_node]:
#             cost_to_next = edges[current_node][next_node]
#             estimated_total = current_cost + cost_to_next + calculate_lower_bound(n, visited, edges)
#
#             # Prune branches with higher cost than current best
#             if estimated_total < best_cost[0]:
#                 visited[next_node] = True
#                 dfs_redone(
#                     start_node,
#                     next_node,
#                     current_cost + cost_to_next,
#                     path + [next_node],
#                     visited,
#                     edges,
#                     best_cost,
#                     best_path
#                 )
#                 visited[next_node] = False  # Backtrack
#
#
#
# def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     stats = []
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     cut_tree = CutTree(len(edges))
#
#     n = len(edges)
#     visited = [False] * n
#     best_cost = [float('inf')]  # Use a mutable object to share state across recursive calls
#     best_path = [[]]  # Use a mutable list to share the best path
#
#     start_node = 0
#     visited[start_node] = True
#     dfs_redone(start_node, start_node, 0, [start_node], visited, edges, best_cost, best_path)
#
#     tour = best_path[0]
#     cost = best_cost[0]
#
#     stats.append(SolutionStats(
#         tour=tour,
#         score=cost,
#         time=timer.time(),
#         max_queue_size=1,
#         n_nodes_expanded=n_nodes_expanded,
#         n_nodes_pruned=n_nodes_pruned,
#         n_leaves_covered=cut_tree.n_leaves_cut(),
#         fraction_leaves_covered=cut_tree.fraction_leaves_covered()
#     ))
#     return stats








# def calculate_lower_bound(n, visited, edges):
#     cost = 0
#     for node in range(0, n - 1):
#         if not visited[node]:
#             cost += min(edges[node][neighbor] for neighbor in range(0, n - 1) if node != neighbor)
#
#     return cost
#
# def dfs_redone(start_node, current_node, current_cost, path, visited, edges, best_cost, best_path):
#     n = len(edges)
#
#     if len(path) == n:
#         total_cost = current_cost + edges[current_node][start_node]
#
#         if total_cost < best_cost:
#             best_cost = total_cost
#             best_path = path + [start_node]
#         return best_cost, best_path
#
#     for next_node in range(0, n - 1):
#         if not visited[next_node]:
#             cost_to_next = edges[current_node][next_node]
#             estimated_total = current_cost + cost_to_next + calculate_lower_bound(next_node, visited, edges)
#
#             if estimated_total < best_cost:
#                 visited[next_node] = True
#                 dfs_redone(start_node, next_node, current_cost + cost_to_next, path + [next_node], visited, edges, best_cost,
#                            best_path)
#                 visited[next_node] = False
#
#     return best_cost, best_path
#
#
#
# def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
#     stats = []
#     n_nodes_expanded = 0
#     n_nodes_pruned = 0
#     cut_tree = CutTree(len(edges))
#     n = len(edges)
#     visited = [False] * n
#     best_cost = float('inf')
#     best_path = []
#     start_node = 0
#
#     visited[start_node] = True
#     best_cost, best_path = dfs_redone(start_node, start_node, 0, [start_node], visited, edges, best_cost, best_path)
#
#
#
#     tour = best_path
#     cost = best_cost
#
#     # cost, tour = dfs_alg(start_node, visited, edges, 0, [])
#     cost = score_tour(tour, edges)
#
#     stats.append(SolutionStats(
#         tour=tour,
#         score=cost,
#         time=timer.time(),
#         max_queue_size=1,
#         n_nodes_expanded=n_nodes_expanded,
#         n_nodes_pruned=n_nodes_pruned,
#         n_leaves_covered=cut_tree.n_leaves_cut(),
#         fraction_leaves_covered=cut_tree.fraction_leaves_covered()
#     ))
#     return stats





def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
