# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


class Node:
    def __init__(self,x, y, clockwise=0, counter_clockwise=0):
        self.x = x
        self.y = y
        self.clockwise = clockwise
        self.counter_clockwise = counter_clockwise

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


def calculate_slope(c: Node,d: Node):
    return (d.getY - c.getY)/(d.getX - c.getX)

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

def calculate_upper(a: Node, b: Node):
# this part will handle the lower bound calculations

    # a = calculate_highest_slope(a,b)
    # b = calculate_highest_slope(b,a)
    a_mod = a
    a_mod2 = a
    
    a_changed = True
    b_changed = True
    while  a_changed == True or b_changed == True:
        
        while a_changed == True :
            a_changed = False
            a_mod.set_clockwise(b)
            a_mod2.set_clockwise(b.get_clockwise)

            if (calculate_slope(a_mod,a_mod.get_clockwise) >= calculate_slope(a_mod2,a_mod2.get_clockwise)):
                a.set_clockwise(a_mod.get_clockwise)
                
            else:
                a.set_clockwise(a_mod2.get_clockwise)
                a_changed = True

        b_mod = a.get_clockwise
        b_mod2 = a.get_clockwise

        while b_changed == True:
            b_changed = False
            b_mod.set_counter_clockwise(a)
            b_mod2.set_counter_clockwise(a.get_counter_clockwise)

            if (calculate_slope(b_mod,b_mod.get_counter_clockwise) >= calculate_slope(b_mod2,b_mod2.get_counter_clockwise)):
                b.set_counter_clockwise(b_mod.get_counter_clockwise)
                
            else:
                b.set_counter_clockwise(b_mod2.get_counter_clockwise)
                b_changed == True

        a_mod = b.get_counter_clockwise
        a_mod2 = b.get_counter_clockwise

    return a,b

def calculate_lower(a: Node, b: Node):
# this part will handle the lower bound calculations

    a_mod = a
    a_mod2 = a
    
    a_changed = True
    b_changed = True
    while  a_changed == True or b_changed == True:
        

            ###KEEP WORKING FROM HERE ON CLOCKWISE V COUNTER CLOCKWISE



        while a_changed == True :
            a_changed = False
            a_mod.set_counter_clockwise(b)
            a_mod2.set_counter_clockwise(b.get_counter_clockwise)

            if (calculate_slope(a_mod,a_mod.get_counter_clockwise) <= calculate_slope(a_mod2,a_mod2.get_counter_clockwise)):
                a.set_counter_clockwise(a_mod.get_counter_clockwise)
                
            else:
                a.set_clockwise(a_mod2.get_clockwise)
                a_changed = True

        b_mod = a.get_clockwise
        b_mod2 = a.get_clockwise

        while b_changed == True:
            b_changed = False
            b_mod.set_counter_clockwise(a)
            b_mod2.set_counter_clockwise(a.get_counter_clockwise)

            if (calculate_slope(b_mod,b_mod.get_counter_clockwise) >= calculate_slope(b_mod2,b_mod2.get_counter_clockwise)):
                b.set_counter_clockwise(b_mod.get_counter_clockwise)
                
            else:
                b.set_counter_clockwise(b_mod2.get_counter_clockwise)
                b_changed == True

        a_mod = b.get_counter_clockwise
        a_mod2 = b.get_counter_clockwise

    return a,b

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

    
    corrected_top_hull = calculate_upper(leftmost_node,rightmost_node)
    
    corrected_bot_hull = calculate_lower(leftmost_node,rightmost_node)



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
        result_list[node.getX(),node.getY()]

    return result_list
