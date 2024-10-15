from numpy.f2py.auxfuncs import throw_error


class ArrayPriorityQueue:

    def __init__(self, nodes):
        self.prio_queue = dict()
        for node in nodes:
            self.prio_queue[node] = None

    def delete_min(self):
        candidate = min(self.prio_queue, key = lambda k: self.prio_queue[k] if self.prio_queue[k] is not None else float('inf'))
        del self.prio_queue[candidate]
        return candidate

    def decrease_key(self,node, v):
        self.prio_queue[node] = v

    def get_length(self):
        return len(self.prio_queue)




class HeapPriorityQueue:

    def __init__(self, nodes):
        self.prio_heap = dict()
        for node in nodes:
            self.prio_heap[node] = None

    def percolate_up(self, index):
        pass

    def percolate_down(self, index):
        pass

    def get_length(self):
        return len(self.prio_heap)

    def delete_min(self):
        pass

    def decrease_key(self, item, priority):
        pass


def dijkstra(graph, source, pq_type) -> tuple[list[int], list[int]]:
    dist = dict()
    prev = dict()
    for u in graph:
        dist[u] = None
        prev[u] = None
    if pq_type == "array":
        H = ArrayPriorityQueue(graph)
    elif pq_type == "heap":
        H = HeapPriorityQueue(graph)
    else:
        throw_error("implementation is not supported")
    dist[source] = 0
    H.decrease_key(source,0)
    while H.get_length() != 0:
        u = H.delete_min()
        for connected_node in graph[u]:
            connection_distance = graph[u][connected_node]
            if dist[connected_node] is None:
                dist[connected_node] = dist[u] + connection_distance
                prev[connected_node] = u
                H.decrease_key(connected_node,connection_distance)
            elif dist[connected_node] > dist[u] + connection_distance:
                dist[connected_node] = dist[u] + connection_distance
                prev[connected_node] = u 
                H.decrease_key(connected_node,connection_distance)
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
    dist, prev = dijkstra(graph, source, "heap")

    cost = dist[target]
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = prev[step]

    return path[::-1], cost



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

    dist, prev = dijkstra(graph, source, "array")
    
    cost = dist[target]
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = prev[step]

    return path[::-1],cost
