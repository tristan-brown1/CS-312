# Uncomment this line to import some functions that can help
# you debug your algorithm
from matplotlib import pyplot as plt

from plotting import draw_line, draw_hull, circle_point,plot_points,show_plot


class Node:
    def __init__(self,x, y, clockwise = None, counter_clockwise = None):
        self.x = x
        self.y = y
        self.clockwise : Node = clockwise
        self.counter_clockwise: Node = counter_clockwise

    def set_clockwise(self, new_node):
        self.clockwise = new_node

    def set_counter_clockwise(self, new_node):
        self.counter_clockwise = new_node
    
    def get_clockwise(self):
        return self.clockwise
    
    def get_counter_clockwise(self):
        return self.counter_clockwise


def calculate_slope(c,d):
    return (c.y - d.y)/(c.x - d.x)


def calculate_lower(a: Node, b: Node):
    either_changed = True
    while either_changed:
        either_changed = False

        if calculate_slope(b, a) > calculate_slope(b, a.counter_clockwise):
            a = a.counter_clockwise
            either_changed = True

        if calculate_slope(b, a) < calculate_slope(b.clockwise, a):
            b = b.clockwise
            either_changed = True

    return a, b


def calculate_upper(a: Node, b: Node):
    either_changed = True
    while either_changed:
        either_changed = False

        if calculate_slope(b, a) < calculate_slope(b, a.clockwise):
            a = a.clockwise
            either_changed = True

        if calculate_slope(b, a) > calculate_slope(b.counter_clockwise, a):
            b = b.counter_clockwise
            either_changed = True

    return a,b


def calculate_rightmost(node_list: list[Node]):
    rightmost_node = None
    for x in node_list:
        if rightmost_node is None:
            rightmost_node = x
        if x.x > rightmost_node.x:
            rightmost_node = x
        else:
            continue
    return rightmost_node
    

def calculate_leftmost(node_list: list[Node]):
    leftmost_node = None
    for x in node_list:
        if leftmost_node is None:
            leftmost_node = x
        if x.x < leftmost_node.x:
            leftmost_node = x
        else:
            continue
    return leftmost_node


def merge_hulls(left_hull,right_hull,corrected_top_left,corrected_top_right,corrected_bot_left,corrected_bot_right):
    merged_list = []

    for i in left_hull:
        if i.x == corrected_top_left.x and i.y == corrected_top_left.y:
            for j in right_hull:
                if j.x == corrected_top_right.x and j.y == corrected_top_right.y:
                    i.set_clockwise(j)
                    j.set_counter_clockwise(i)
                    merged_list.append(j)
                    merged_list.append(i)
        if i.x == corrected_bot_left.x and i.y == corrected_bot_left.y:
            for j in right_hull:
                if j.x == corrected_bot_right.x and j.y == corrected_bot_right.y:
                    i.set_counter_clockwise(j)
                    j.set_clockwise(i)

    next_one = merged_list[1]
    while next_one != merged_list[0]:
        if next_one != merged_list[1]:
            merged_list.append(next_one)
        next_one = next_one.get_counter_clockwise()

    return merged_list


def hull_algorithm(node_list):
    n = len(node_list)
    new_list = []
    if n == 1:
        new_node = Node(node_list[0][0], node_list[0][1])
        new_node.set_clockwise(new_node)
        new_node.set_counter_clockwise(new_node)
        new_list.append(new_node)
        return new_list

    L = node_list[:n//2]
    R = node_list[n//2:]

    left_hull = hull_algorithm(L)
    right_hull = hull_algorithm(R)

    leftmost_node = calculate_leftmost(right_hull)
    rightmost_node = calculate_rightmost(left_hull)

    temp_leftmost  = Node(leftmost_node.x,leftmost_node.y,leftmost_node.clockwise,leftmost_node.counter_clockwise)
    temp_rightmost  = Node(rightmost_node.x,rightmost_node.y,rightmost_node.clockwise,rightmost_node.counter_clockwise)

    corrected_top_right, corrected_top_left = calculate_upper(leftmost_node,rightmost_node)
    corrected_bot_right, corrected_bot_left = calculate_lower(temp_leftmost,temp_rightmost)

    new_node_list = merge_hulls(left_hull,right_hull,corrected_top_left,corrected_top_right,corrected_bot_left,corrected_bot_right)

    return new_node_list


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    result_list = []

    linked_list = hull_algorithm(sorted(points))

    for node in linked_list:
        result_list.append((node.x, node.y))

    return result_list
