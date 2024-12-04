## Component class and its subclasses
# Component class is the parent class of Conductor, Resistor, and Supply classes.
# A Component is an object that represents a physical component in an electrical circuit.
# It has an id, start position, end position, a list of node ids, and the id of the branch
# it belongs to. The Component class has methods to change the branch, add a node id, remove
# a node id, change the start position, and change the end position of the component.

# The Conductor, Resistor, and Supply classes are subclasses of the Component class.
# They inherit the attributes and methods of the Component class and will have additional
# attributes and methods specific to their type.




class Component:
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        self.id = id
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.component_type = None
        self.node_ids = node_ids
        self.branch_id = branch_id
    
    # Changes the branch id of the component to the new branch id   
    def change_branch(self, new_branch_id):
        self.branch_id = new_branch_id


    

class Conductor(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)


class Resistor(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)

    
class Supply(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)

# Creates a new component with the given id, start position, end position, node ids, and 
# branch id. The component type is used to determine which subclass of the Component class
# to create.
def add_component(component_type, id, start_pos, end_pos, node_ids=[], branch_id=None):

    if component_type == 'Conductor':
        return Conductor(id, start_pos, end_pos, node_ids, branch_id)
    elif component_type == 'Resistor':
        return Resistor(id, start_pos, end_pos, node_ids, branch_id)
    elif component_type == 'Supply':
        return Supply(id, start_pos, end_pos, node_ids, branch_id)
    elif component_type == None:
        return Component(id, start_pos, end_pos, node_ids, branch_id)

def add_node_id(component, node_id):
    component.node_ids.append(node_id)

def remove_node(component, node_id):
    component.node_ids.remove(node_id)

def change_start_pos(component, new_pos):
    component.start_pos = new_pos

def change_end_pos(component, new_pos):
    component.end_pos = new_pos

    
def component_by_id(components, component_id):
    return [component for component in components if component.id == component_id]

def change_id(component, new_id):
    component.id = new_id
