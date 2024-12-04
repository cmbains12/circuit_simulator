



class Node:
    def __init__(self, id, pos, branch_id=None):
        self.id = id
        self.pos = pos
        self.component_ids = []
        self.branch_id = branch_id
        
    def change_branch(self, new_branch_id):
        self.branch_id = new_branch_id

def add_component_id(Node, component_id):
    Node.component_ids.append(component_id)

def remove_component_id(node, component_id):
    node.component_ids.remove(component_id)

def change_pos(node, new_pos):
    node.pos = new_pos



def add_node(id, pos, branch_id):
    return Node(id, pos, branch_id)






