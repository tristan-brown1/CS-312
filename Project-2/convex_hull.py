# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


class Node:
    def __init__(self,x, y, right=0, left=0):
        self.x = x
        self.y = y
        self.right = right
        self.left = left

    def set_right(self, new_node):
        self.right = new_node

    def set_left(self, new_node):
        self.left = new_node

    def getX(self):
        return self.x
    def getY(self):
        return self.y

def calculate_upper():
# this part will handle the lower bound calculations


    pass

def calculate_lower():
# this part will handle the upper bound calculations


    pass

def calculate_rightmost():

    pass

def calculate_leftmost():

    pass

def hull_algorithm(node_list: list[Node]):
# this part will handle the linked list and recurse
    n = len(node_list)
    if n == 1:
        return node_list

    L = node_list[0:n/2]
    R = node_list[n/2:]

    left_hull = hull_algorithm(L)
    right_hull = hull_algorithm(R)

    


    return node_list

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    linked_list = []
    result_list = []
    for element in sorted(points):
        new_node = Node(element[0], element[1])
        new_node.set_right(new_node)
        new_node.set_left(new_node)
        linked_list.append(new_node)


    linked_list = hull_algorithm(linked_list)

    for node in linked_list:
        result_list[node.getX(),node.getY()]

    return result_list
