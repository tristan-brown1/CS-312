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

    def __init__(self, nodes, source):
        self.heap_list = []
        self.index_dict = dict()
        self.history = set()

        # self.heap_list.append(0,source)
        # self.index_dict[0] = source

        # for node in nodes:
        #     i = 1
        #     if node == source:
        #         pass
        #     else:
        #         self.heap_list.append(None,node)
        #         self.index_dict[node] = i
        #         i += 1

    # def insert(self, node):
    #     self.heap_list.append(None,node)
    #     self.index_dict[node] = i

    def swap_up(self, index):
        pass

    def swap_down(self, index):
        pass

    def swap(self,i,j):
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]
        self.index_dict[self.heap_list[i][1]] = self.heap_list[j][0]   
        self.index_dict[self.heap_list[j][1]] = self.heap_list[j][0]

    def get_length(self):
        return len(self.heap_list)

    def delete_min(self):
        min = self.heap_list[0]
        del self.index_dict[min[1]]
        self.heap_list[0] = self.heap_list[-1]
        self.heap_list.pop

        settled = False
        while settled != True:
            settled = True
            if self.heap_listp[1] < self.heap_list[2]:
                if self.heap_list[0] < self.heap_list[1]:
                    self.swap(0,1)
                    settled = False
            else:
                if self.heap_list[0] < self.heap_list[2]:
                    self.swap(0,2)
                    settled = False
                


        # settled = False
        # while settled != True:
        #     pass


    def decrease_key(self, node, distance):
        self.heap_list.append(distance,node)
        self.index_dict[len(self.heap_list) - 1] = node


def dijkstra(graph, source, pq_type) -> tuple[list[int], list[int]]:
    dist = dict()
    prev = dict()
    for u in graph:
        dist[u] = None
        prev[u] = None
    if pq_type == "array":
        H = ArrayPriorityQueue(graph)
    elif pq_type == "heap":
        H = HeapPriorityQueue(graph,source)
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
