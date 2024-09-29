# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


def node():
    def __init__(self,x, y, right, left):
        self.x = x
        self.y = y
        self.right = right
        self.left = left
    
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

def hull_algorithm():
# this part will handle the linked list and recurse
    pass

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    linked_list = []
    result_list = []
    for tuple in list:
        linked_list.append(node(tuple[0],tuple[1]))

    linked_list = hull_algorithm(linked_list)

    for node in linked_list:
        result_list[node.getX,node.getY]

    return [result_list]
