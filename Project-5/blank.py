import numpy as np
import heapq


class BranchAndBoundTSP:
    def __init__(self, cost_matrix):
        self.n = len(cost_matrix)
        self.cost_matrix = np.array(cost_matrix, dtype=float)
        self.bssf = float('inf')  # Best solution so far (minimized cost)
        self.best_path = None  # Store the best path found

    def calculate_reduced_cost_matrix(self, matrix):
        matrix = np.array(matrix, dtype=float)
        n = matrix.shape[0]
        reduced_matrix = matrix.copy()
        reduction_cost = 0

        # Row reduction
        for i in range(n):
            row_min = np.min(reduced_matrix[i, :])
            if row_min < np.inf:
                reduced_matrix[i, :] -= row_min
                reduction_cost += row_min

        # Column reduction
        for j in range(n):
            col_min = np.min(reduced_matrix[:, j])
            if col_min < np.inf:
                reduced_matrix[:, j] -= col_min
                reduction_cost += col_min

        return reduced_matrix, reduction_cost

    def branch_and_bound_search (self):
        # Initialize the stack for DFS
        stack = []

        # Calculate the initial reduced cost matrix and its cost
        reduced_matrix, reduction_cost = self.calculate_reduced_cost_matrix(self.cost_matrix)
        initial_state = {
            "path": [0],  # Start from city 0
            "reduced_matrix": reduced_matrix,
            "cost": reduction_cost,
            "lower_bound": reduction_cost
        }

        # Push the initial state to the stack
        stack.append(initial_state)

        while stack:
            # Pop the top state from the stack (DFS)
            state = stack.pop()
            current_path = state["path"]
            current_matrix = state["reduced_matrix"]
            current_cost = state["cost"]

            # If the path is complete, check if it's the best solution
            if len(current_path) == self.n:
                total_cost = current_cost + current_matrix[current_path[-1], 0]  # Add cost to return to start
                if total_cost < self.bssf:
                    self.bssf = total_cost
                    self.best_path = current_path
                continue

            # Expand the current state
            for next_city in range(self.n):
                if next_city not in current_path:
                    new_path = current_path + [next_city]

                    # Create a new reduced cost matrix
                    new_matrix = current_matrix.copy()

                    # Set the row and column of the current city and next city to infinity
                    new_matrix[current_path[-1], :] = np.inf
                    new_matrix[:, next_city] = np.inf
                    new_matrix[next_city, current_path[-1]] = np.inf

                    # Reduce the new matrix
                    reduced_matrix, reduction_cost = self.calculate_reduced_cost_matrix(new_matrix)
                    new_cost = current_cost + current_matrix[current_path[-1], next_city] + reduction_cost
                    lower_bound = new_cost

                    # Prune states with a lower bound greater than the BSSF
                    if lower_bound < self.bssf:
                        new_state = {
                            "path": new_path,
                            "reduced_matrix": reduced_matrix,
                            "cost": new_cost,
                            "lower_bound": lower_bound
                        }
                        stack.append(new_state)

    def branch_and_bound(self):
        stats = []
        self.branch_and_bound_search()

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


# Example Usage
if __name__ == "__main__":
    cost_matrix = [
        [np.inf, 20, 30, 10],
        [10, np.inf, 15, 25],
        [30, 15, np.inf, 20],
        [10, 25, 20, np.inf]
    ]

    tsp_solver = BranchAndBoundTSP(cost_matrix)
    best_cost, best_path = tsp_solver.solve()
    print("Best Cost:", best_cost)
    print("Best Path:", best_path)
