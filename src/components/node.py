## Node class definition and methods
# A Node is an object that represents a node in an electrical circuit. It has an id, position, 
# a list of component ids, and the id of the net it belongs to. The Node class has methods 
# to change the net, add a component id, remove a component id, and change the position of 
# the node.



class Node:
    def __init__(self, id, pos, net_id=None):
        self.id = id
        self.pos = pos
        self.component_ids = []
        self.net_id = net_id
        
    def change_net(self, new_net_id):
        self.net_id = new_net_id

def add_component_id(Node, component_id):
    Node.component_ids.append(component_id)

def remove_component_id(node, component_id):
    node.component_ids.remove(component_id)

def change_pos(node, new_pos):
    node.pos = new_pos



def add_node(id, pos, net_id):
    return Node(id, pos, net_id)






