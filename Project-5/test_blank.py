import numpy as np
from tsp_solve import greedy_tour, dfs, branch_and_bound, branch_and_bound_smart, calculate_reduced_cost_matrix

def test_matrix():
    # Example matrix
    matrix = [
        [np.inf, 20, 30, 10],
        [10, np.inf, 15, 25],
        [30, 15, np.inf, 20],
        [10, 25, 20, np.inf]
    ]

    reduced_matrix, reduction_cost = calculate_reduced_cost_matrix(matrix)
    print("Reduced Cost Matrix:")
    print(matrix)
    print(reduced_matrix)
    print("Reduction Cost:", reduction_cost)

