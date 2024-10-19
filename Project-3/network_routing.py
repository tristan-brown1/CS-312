
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

    def get_length(self):
        return len(self.prio_queue)

    def decrease_key(self,node, distance):
        self.prio_queue[node] = distance


class HeapPriorityQueue:

    def __init__(self, nodes):
        self.heap_list: [tuple[float,int]] = []
        self.index_dict = dict()
        self.history = set()

    def swap_up(self, index):
        parent_index = ((index + 1) //2)
        if parent_index == 0:
            return
        else:
            parent_index -= 1

        parent = self.heap_list[parent_index]
        candidate = self.heap_list[index]

        if parent[0] > candidate[0]:
            self.swap(parent_index,index)
            self.swap_up(parent_index)

    def swap_down(self, index):
        candidate = self.heap_list[index]
        child_A_index = (index + 1) * 2 - 1
        child_B_index = (index + 1) * 2

        if child_A_index < len(self.heap_list):
            child_A = self.heap_list[child_A_index]
        else:
            child_A = None

        if child_B_index < len(self.heap_list):
            child_B = self.heap_list[child_B_index]
        else:
            child_B = None

        if child_A is None:
            return
        elif child_B is None:
            if child_A[0] < candidate[0]:
                self.swap(index, child_A_index)
                self.swap_down(child_A_index)
        else:
            if child_A[0] < candidate[0] or child_B[0] < candidate[0]:
                if child_A[0] < child_B[0]:
                    self.swap(index, child_A_index)
                    self.swap_down(child_A_index)
                else:
                    self.swap(index, child_B_index)
                    self.swap_down(child_B_index)

    def swap(self,i,j):
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]
        self.index_dict[self.heap_list[i][1]] = i  
        self.index_dict[self.heap_list[j][1]] = j

    def get_length(self):
        return len(self.heap_list)

    def delete_min(self):

        min_node = self.heap_list[0]
        del self.index_dict[min_node[1]]
        self.heap_list[0] = self.heap_list[-1]
        self.heap_list.pop()
        self.history.add(min_node[1])

        if len(self.heap_list) > 1:
            self.index_dict[self.heap_list[0][1]] = 0
            self.swap_down(0)

        elif len(self.heap_list) > 0:
            last_value = self.heap_list[0][1]
            self.index_dict[last_value] = 0

        return min_node[1]

    def decrease_key(self, node, distance):

        if node in self.heap_list:
            current_index = self.index_dict[node]
            if distance < self.heap_list[current_index][0]:
                self.heap_list[current_index][0] = distance
                self.swap_up(current_index)
        elif node not in self.history:
            self.heap_list.append([distance,node])
            self.index_dict[node] = len(self.heap_list) - 1
            self.swap_up(len(self.heap_list) - 1)


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
            if dist[u] is not None:
                if dist[connected_node] is None:
                    dist[connected_node] = dist[u] + connection_distance
                    prev[connected_node] = u
                    H.decrease_key(connected_node,dist[u] + connection_distance)
                elif dist[connected_node] > dist[u] + connection_distance:
                    dist[connected_node] = dist[u] + connection_distance
                    prev[connected_node] = u
                    H.decrease_key(connected_node,dist[u] + connection_distance)

    return dist,prev


def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:

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

    dist, prev = dijkstra(graph, source, "array")
    
    cost = dist[target]
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = prev[step]

    return path[::-1],cost
