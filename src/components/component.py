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
    def __init__(self, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]):
        self.id = id
        self.branch_id = brch_id
        self.start_pos = st_pos
        self.end_pos = nd_pos
        self.node_ids = nd_ids
        self.net_id = nt_id
        self.mesh_ids = msh_ids
        self.net_type = nt_type
        
    def get_id(self):
        compid = self.id
        return compid
    
    def get_branch_id(self):
        branch_id = self.branch_id
        return branch_id
    
    def get_net_id(self):
        net_id = self.net_id
        return net_id
    
    def get_node_ids(self):
        node_ids = self.node_ids
        return node_ids
    
    def get_start_pos(self):
        start_pos = self.start_pos
        return start_pos
    
    def get_end_pos(self):
        end_pos = self.end_pos
        return end_pos
    
    def get_mesh_ids(self):
        mesh_ids = self.mesh_ids
        return mesh_ids
    
    def change_branch_id(self, new_id):
        self.branch_id = new_id
        
    def change_net_id(self, new_id):
        self.net_id = new_id
        
    def change_node_id(self, old_id, new_id):
        self.node_ids[self.node_ids.index(old_id)] = new_id
        
    def change_start_pos(self, new_pos):
        self.start_pos = new_pos
        
    def change_end_pos(self, new_pos):
        self.end_pos = new_pos
        
    def add_mesh_id(self, msh_id):
        self.mesh_ids.append(msh_id)
        
    def remove_mesh_id(self, msh_id):
        self.mesh_ids.remove(msh_id)
        
    def add_node_id(self, nd_id):
        self.node_ids.append(nd_id)
        
    def set_net_type(self, nt_type):
        self.net_type = nt_type
        
    def get_net_type(self):
        return self.net_type
        
        
class Conductor(Component):
    def __init__(self, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]):
        super().__init__(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)


class Resistor(Component):
    def __init__(self, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]):
        super().__init__(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)

    
class Supply(Component):
    def __init__(self, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]):
        super().__init__(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)

# Creates a new component with the given id, start position, end position, node ids, and 
# net id. The component type is used to determine which subclass of the Component class
# to create.
def add_component(type, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]):

    if type == 'Conductor':
        return Conductor(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)
    elif type == 'Resistor':
        return Resistor(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)
    elif type == 'Supply':
        return Supply(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids)
    elif type == None:
        return Component(id, brch_id, nt_id, st_pos, nd_pos, msh_ids, nt_type, nd_ids) 

