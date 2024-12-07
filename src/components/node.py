## Node class definition and methods
# A Node is an object that represents a node in an electrical circuit. It has an id, position, 
# a list of component ids, and the id of the net it belongs to. The Node class has methods 
# to change the net, add a component id, remove a component id, and change the position of 
# the node.



class Node:
    def __init__(self, id, brch_id, nt_id, cmp_ids, pos, msh_ids=None):
        self.id = id
        self.branch_id = brch_id
        self.net_id = nt_id
        self.component_ids = [cmp_ids]
        self.pos = pos
        self.mesh_ids = [msh_ids]
        
    def get_id(self):
        return self.id
    
    def get_branch_id(self):
        return self.branch_id
    
    def get_net_id(self):
        return self.net_id
    
    def get_component_ids(self):
        return self.component_ids
    
    def get_position(self):
        return self.pos
    
    def get_mesh_ids(self):
        return self.mesh_ids
    
    def change_branch_id(self, new_id):
        self.branch_id = new_id
        
    def change_net_id(self, new_id):
        self.net_id = new_id
        
    def add_component_id(self, cmp_id):
        self.component_ids.append(cmp_id)
        
    def remove_component_id(self, cmp_id):
        self.component_ids.remove(cmp_id)
        
    def change_position(self, new_pos):
        self.pos = new_pos
        
    def add_mesh_id(self, msh_id):
        self.mesh_ids.append(msh_id)
        
    def remove_mesh_id(self, msh_id):
        self.mesh_ids.remove(msh_id)
        
def add_node(id, brch_ids, nt_id, cmp_ids, pos, msh_ids=None):
    
    return Node(id, brch_ids, nt_id, cmp_ids, pos, msh_ids)

                
                
        







