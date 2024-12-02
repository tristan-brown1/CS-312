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
            # no valid path remaining
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

    i = 0
    while True:
        if timer.time_out():
            return stats


        potential_tour = greedy_pathfinder(i, edges)
        if potential_tour is None:
            i += 1
            continue
        else:
            tour = greedy_pathfinder(i, edges)
            cost = score_tour(tour, edges)

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


def dfs_alg(start_node, visited, edges, current_cost, path):
    current_node = start_node
    if all(visited):
        return current_cost + edges[current_node][start_node], path

    min_cost = float('inf')
    min_cost_path = []

    for next_city in range(0, len(edges)):
        if not visited[next_city]:
            visited[next_city] = True
            cost = edges[current_node][next_city]
            total_cost, sub_path = dfs_alg(next_city, visited, edges, current_cost + cost, path + [next_city])
            if total_cost < min_cost:
                min_cost = total_cost
                min_cost_path = sub_path
            visited[next_city] = False
    return min_cost, min_cost_path

def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    start_node = 0
    visited = [False] * len(edges)
    dfs_answer = dfs_alg(start_node, visited, edges, 0, [])
    tour = dfs_answer[1]
    cost = score_tour(tour, edges)



    # take current dfs implementation and move the calculation of the min path to this part of the logic


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


def reduce_matrix(matrix) -> tuple[float, list[SolutionStats]]:

    pass

def expand() -> list[SolutionStats]:

    pass

def bnb_logic(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    pass

def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    #clean up dfs logic get it completely fleshed out and clean

    #write out hollow bnb logic using dfs but with updated lower bound in order to prune the queue that feeds into bnb

    #flesh out elements added from bnb
        #reduce matrix
        #extracting lower bound
        #bnb logic




    start_node = 0
    visited = [False] * len(edges)
    cost, tour = dfs_alg(start_node, visited, edges, 0, [])
    cost = score_tour(tour, edges)

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





def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []
