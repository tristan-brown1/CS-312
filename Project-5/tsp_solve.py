import math
import random

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


def dfs_recursion(start_node, visited, edges, current_cost, path, all_paths):
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
            dfs_recursion(next_city, visited, edges, current_cost + edges[current_node][next_city], path, all_paths)
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
    dfs_recursion(start_node, visited, edges, 0, [], all_paths)

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
    n = len(edges)
    reduced_matrix = [[0] * n for _ in range(n)]

    # row reduction
    for i in range(n):
        min_row_value = min(edges[i])
        for j in range(n):
            reduced_matrix[i][j] = edges[i][j] - min_row_value

    min_col_values = [min(reduced_matrix[i][j] for i in range(n)) for j in range(n)]

    # column reduction
    for j in range(n):
        for i in range(n):
            reduced_matrix[i][j] -= min_col_values[j]

    return reduced_matrix

def calculate_lower_bound(n, visited, edges):
    reduced_cost_matrix = reduce_matrix(edges)

    cost = 0
    for node in range(n):
        if not visited[node]:
            min_cost = float('inf')
            for neighbor in range(n):
                if not visited[neighbor] and neighbor != node:
                    min_cost = min(min_cost, reduced_cost_matrix[node][neighbor])
            cost += min_cost if min_cost != float('inf') else 0
    return cost

def dfs_redone(node, cost, path, visited, edges, best_cost, best_path, timer,
               n_nodes_expanded, n_nodes_pruned):
    if timer.time_out():
        return

    n = len(edges)

    # base case
    if len(path) == n:
        total_cost = cost + edges[node][path[0]]
        if total_cost < best_cost[0]:
            best_cost[0] = total_cost
            best_path[0] = path.copy()
        return

    lower_bound = calculate_lower_bound(n, visited, edges)

    # explore unvisited nodes
    for next_node in range(n):
        if visited[next_node]:
            continue

        est_cost = cost + edges[node][next_node] + lower_bound
        if est_cost < best_cost[0]:
            visited[next_node], path_appended = True, next_node
            path.append(path_appended)
            n_nodes_expanded[0] += 1

            dfs_redone(next_node, cost + edges[node][next_node], path, visited, edges,
                       best_cost, best_path, timer, n_nodes_expanded, n_nodes_pruned)

            path.pop()
            visited[next_node] = False
        else:
            n_nodes_pruned[0] += 1




def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    visited = [False] * len(edges)
    greedy_result = greedy_tour(edges, timer)
    best_cost = [greedy_result[0].score]
    best_path = [greedy_result[0].tour]
    n_nodes_expanded = [0]
    n_nodes_pruned = [0]
    cut_tree = CutTree(len(edges))

    visited[0] = True
    dfs_redone( 0, 0, [0], visited, edges, best_cost, best_path, timer, n_nodes_expanded, n_nodes_pruned)

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


def local_search(tour, edges):
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
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(n)
    greedy_result = greedy_tour(edges, timer)
    best_path = greedy_result[0].tour
    best_path = local_search(best_path, edges)
    best_cost = score_tour(best_path, edges)
    prio_queue = [(best_cost, best_path, [False] * n)]

    while prio_queue and not timer.time_out():

        prio_queue.sort(key=lambda x: x[0])
        current_cost, path, visited = prio_queue.pop(0)

        if len(path) == n:
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = path
            continue

        for next_node in range(n):
            if not visited[next_node]:
                next_cost = current_cost + edges[path[-1]][next_node]
                next_visited = visited[:]
                next_visited[next_node] = True
                next_path = path + [next_node]

                if next_cost < best_cost:
                    prio_queue.append((next_cost, next_path, next_visited))
                    n_nodes_expanded += 1
                else:
                    n_nodes_pruned += 1

    stats.append(SolutionStats(
        tour=best_path,
        score=best_cost,
        time=timer.time(),
        max_queue_size=len(prio_queue),
        n_nodes_expanded=n_nodes_expanded,
        n_nodes_pruned=n_nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    ))

    return stats