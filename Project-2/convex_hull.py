# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


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

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def get_clockwise(self):
        return self.clockwise
    
    def get_counter_clockwise(self):
        return self.counter_clockwise




def calculate_slope(c,d):
    return (c.y - d.y)/(c.x - d.x)

# def calculate_highest_slope(a: Node, b: Node):
#     a_mod = a
#     a_mod2 = a
    
#     a_mod.set_clockwise(b)
#     a_mod2.set_clockwise(b.get_clockwise)

#     if (calculate_slope(a_mod,a_mod.get_clockwise) >= calculate_slope(a_mod2,a_mod2.get_clockwise)):
#         a.set_clockwise(a_mod.get_clockwise)
#     else:
#         a.set_clockwise(a_mod2.get_clockwise)

#     return a 

def calculate_lower(h: Node, k: Node):
# this part will handle the lower bound calculations
    a = h
    b = k
    a_changed = True
    b_changed = True

    while  a_changed == True or b_changed == True:
        a_mod = Node(a.x,a.y,a.clockwise,a.counter_clockwise)
        a_mod2 = Node(a.x,a.y,a.clockwise,a.counter_clockwise)
        
        while a_changed:
            a_changed = False
            a_mod.set_clockwise(b)
            a_mod2.set_clockwise(b.get_clockwise())

            if calculate_slope(a_mod, a_mod.get_clockwise()) >= calculate_slope(a_mod2, a_mod2.get_clockwise()):
                a.set_clockwise(a_mod.get_clockwise())
                
            else:
                a.set_clockwise(a_mod2.get_clockwise())
                b = a_mod2.get_clockwise()
                a_changed = True

        b_mod = Node(b.x,b.y,b.clockwise,b.counter_clockwise)
        b_mod2 = Node(b.x,b.y,b.clockwise,b.counter_clockwise)

        while b_changed:
            b_changed = False
            b_mod.set_counter_clockwise(a)
            b_mod2.set_counter_clockwise(a.get_counter_clockwise())

            if calculate_slope(b_mod, b_mod.get_counter_clockwise()) <= calculate_slope(b_mod2, b_mod2.get_counter_clockwise()):
                b.set_counter_clockwise(b_mod.get_counter_clockwise())
                
            else:
                b.set_counter_clockwise(b_mod2.get_counter_clockwise())
                a = b_mod2.get_counter_clockwise()
                b_changed = True

    return a,b

def calculate_upper(f: Node, g: Node):
# this part will handle the lower bound calculations
    a = f
    b = g
    a_changed = True
    b_changed = True

    while  a_changed == True or b_changed == True:

        a_mod = Node(a.x, a.y, a.clockwise, a.counter_clockwise)
        a_mod2 = Node(a.x, a.y, a.clockwise, a.counter_clockwise)

        while a_changed:
            a_changed = False
            a_mod.set_counter_clockwise(b)
            a_mod2.set_counter_clockwise(b.get_counter_clockwise())

            if calculate_slope(a_mod, a_mod.get_counter_clockwise()) <= calculate_slope(a_mod2, a_mod2.get_counter_clockwise()):
                a.set_counter_clockwise(a_mod.get_counter_clockwise())
                
            else:
                a.set_counter_clockwise(a_mod2.get_counter_clockwise())
                b = a_mod2.get_counter_clockwise()
                a_changed = True

        b_mod = Node(b.x, b.y, b.clockwise, b.counter_clockwise)
        b_mod2 = Node(b.x, b.y, b.clockwise, b.counter_clockwise)

        while b_changed:
            b_changed = False
            b_mod.set_clockwise(a)
            b_mod2.set_clockwise(a.get_clockwise())

            if calculate_slope(b_mod, b_mod.get_clockwise()) >= calculate_slope(b_mod2, b_mod2.get_clockwise()):
                b.set_clockwise(b_mod.get_clockwise())
                
            else:
                b.set_clockwise(b_mod2.get_clockwise())
                a = b_mod2.get_clockwise()
                b_changed = True

    return a,b

def calculate_rightmost(node_list: list[Node]):
    rightmost_node = None
    for x in node_list:
        if rightmost_node is None:
            rightmost_node = x
        elif x.x > rightmost_node.x:
            rightmost_node = x
        else:
            continue
    return rightmost_node
    

def calculate_leftmost(node_list: list[Node]):
    leftmost_node = None
    for x in node_list:
        if leftmost_node is None:
            leftmost_node = x
        elif x.x < leftmost_node.x:
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
                    merged_list.append(i)
                    merged_list.append(j)
        if i.x == corrected_bot_left.x and i.y == corrected_bot_left.y:
            for j in right_hull:
                if j.x == corrected_bot_right.x and j.y == corrected_bot_right.y:
                    i.set_counter_clockwise(j)
                    j.set_clockwise(i)


    next_one = merged_list[1]
    while next_one != merged_list[0]:
        if next_one != merged_list[1]:
            merged_list.append(next_one)
        next_one = next_one.get_clockwise()

    return merged_list

def hull_algorithm(node_list: list[Node]):
# this part will handle the linked list and recurse
    n = len(node_list)
    if n == 1:
        return node_list

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

    node_list = merge_hulls(left_hull,right_hull,corrected_top_left,corrected_top_right,corrected_bot_left,corrected_bot_right)

    return node_list

def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    linked_list = []
    result_list = []

    for element in sorted(points):
        new_node = Node(element[0], element[1])
        new_node.set_clockwise(new_node)
        new_node.set_counter_clockwise(new_node)
        linked_list.append(new_node)

    linked_list = hull_algorithm(linked_list)

    for node in linked_list:
        result_list.append((node.x, node.y))

    return result_list
