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
    
    def get_right(self):
        return self.right
    
    def get_left(self):
        return self.left


def calculate_slope(c: Node,d: Node):
    return (c.getX - d.getX)/(c.getY - d.getY)

def calculate_upper(a: Node, b: Node):
# this part will handle the lower bound calculations
    a_mod = a
    b_mod = b
    a_mod2 = a
    b_mod2 = b

    a_mod.set_right(b_mod)
    a_mod2.set_right(b_mod.get_right)
    if (calculate_slope()):
        pass

    return a,b

def calculate_lower():
# this part will handle the upper bound calculations


    pass

def calculate_rightmost(node_list: list[Node]):
    rightmost_node = None
    for x in node_list:
        if rightmost_node == None:
            rightmost_node = x.x
        if x.x > rightmost_node:
            rightmost_node = x.x
        else:
            continue
    return rightmost_node
    

def calculate_leftmost(node_list: list[Node]):
    leftmost_node = None
    for x in node_list:
        if leftmost_node == None:
            leftmost_node = x.x
        if x.x < leftmost_node:
            leftmost_node = x.x
        else:
            continue
    return leftmost_node

def hull_algorithm(node_list: list[Node]):
# this part will handle the linked list and recurse
    n = len(node_list)
    if n == 1:
        return node_list

    L = node_list[0:n/2]
    R = node_list[n/2:]

    left_hull = hull_algorithm(L)
    right_hull = hull_algorithm(R)

    leftmost_node = calculate_leftmost(right_hull)
    rightmost_node = calculate_rightmost(left_hull)

    calculate_upper
    
    calculate_lower


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
