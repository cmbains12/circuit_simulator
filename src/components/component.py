



class Component:
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        self.id = id
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.component_type = None
        self.node_ids = node_ids
        self.branch_id = branch_id
        
    def change_branch(self, new_branch_id):
        self.branch_id = new_branch_id


    

class Conductor(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)
        self.component_type = 'Conductor'

class Resistor(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)
        self.component_type = 'Resistor'
    
class Supply(Component):
    def __init__(self, id, start_pos, end_pos, node_ids=[], branch_id=None):
        super().__init__(id, start_pos, end_pos, node_ids, branch_id)
        self.component_type = 'Supply'

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
