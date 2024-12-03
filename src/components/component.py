



class Component:
    def __init__(self, id, start_pos, end_pos, nodes=[], branch=None):
        self.id = id
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.component_type = None
        self.nodes = nodes
        self.branch = branch


    

class Conductor(Component):
    def __init__(self, id, start_pos, end_pos):
        super().__init__(id, start_pos, end_pos)
        self.component_type = 'Conductor'

class Resistor(Component):
    def __init__(self, id, start_pos, end_pos):
        super().__init__(id, start_pos, end_pos)
        self.component_type = 'Resistor'
    
class Supply(Component):
    def __init__(self, id, start_pos, end_pos):
        super().__init__(id, start_pos, end_pos)
        self.component_type = 'Supply'

def add_component(component_type, id, start_pos, end_pos):

    if component_type == 'Conductor':
        return Conductor(id, start_pos, end_pos)
    elif component_type == 'Resistor':
        return Resistor(id, start_pos, end_pos)
    elif component_type == 'Supply':
        return Supply(id, start_pos, end_pos)
    elif component_type == None:
        return Component(id, start_pos, end_pos)

def add_node_id(component, node_id):
    component.nodes.append(node_id)

def remove_node(component, node_id):
    component.nodes.remove(node_id)

def change_start_pos(component, new_pos):
    component.start_pos = new_pos

def change_end_pos(component, new_pos):
    component.end_pos = new_pos

def change_branch(component, new_branch):
    component.branch = new_branch