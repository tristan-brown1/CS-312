
class Array_priority_queue:

    def _init_(self, nodes):
        self.prio_queue = dict()
        i = 0
        for node in nodes:
            self.prio_queue[i] = node
            i += 1

    def delete_min(self):
        candidate = min(self.prio_queue, key = self.prio_queue.get)
        del self.prio_queue[candidate]
        return candidate

    def decrease_key(self, v):
        pass




def dijkstra(graph,source) -> tuple[list[int], list[int]]:
    dist = dict()
    prev = dict()
    for u in graph:
        dist[u] = None
        prev[u] = None
    dist[source] = 0
    H = Array_priority_queue(graph)
    while len(H) != 0:
        u = H.delete_min()
        for u,v in graph:
            if dist[v] > dist[u] + len(u,v):
                dist[v] = dist[u] + len(u,v)
                prev[v] = u 
                H.decrease_key(v)
    return dist,prev





def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """


def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:

    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    dist, prev = dijkstra(graph, source)
    cost = dist[target]
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = prev[step]

    return path[::-1],cost
