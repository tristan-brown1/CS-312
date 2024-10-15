
class Array_priority_queue:

    def _init_(self, nodes):
        self.prio_queue = dict()
        for node in nodes:
            self.prio_queue[node[0]] = None

    def delete_min(self):
        candidate = min(self.prio_queue, key = self.prio_queue.get)
        del self.prio_queue[candidate]
        return candidate

    def decrease_key(self,node, v):
        self.prio_queue[node] = v




def dijkstra(graph,source) -> tuple[list[int], list[int]]:
    dist = dict()
    prev = dict()
    for u in graph:
        dist[u[0]] = None
        prev[u[0]] = None
    H = Array_priority_queue(graph)
    dist[source] = 0
    H.decrease_key(source,0)
    while len(H) != 0:
        u = H.delete_min()
        for connected_node,connection_distance in graph[u]:
            if dist[connected_node] == None:
                dist[connected_node] = connection_distance
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
    while step != None:
        path.append(step)
        step = prev[step]

    return path[::-1],cost
