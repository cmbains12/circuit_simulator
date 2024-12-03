



class Node:
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.components = []
        self.branch = None

def add_component_id(Node, component_id):
    Node.components.append(component_id)

def remove_component_id(node, component_id):
    node.components.remove(component_id)

def change_pos(node, new_pos):
    node.pos = new_pos

def change_branch(node, new_branch):
    node.branch = new_branch

def add_node(id, pos):
    return Node(id, pos)






