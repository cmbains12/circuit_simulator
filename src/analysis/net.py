## Net class and functions
# Net class is used to store the components that are connected to each other.
# Each net has an id and a list of component ids.


class Net():
    def __init__(self, id, brch_ids, cmp_ids, nd_ids, msh_ids = []):
        self.id = id
        self.branch_ids = [brch_ids]
        self.component_ids = [cmp_ids]
        self.node_ids = [nd_ids]
        self.mesh_ids = [msh_ids]
    
    # Returns the list of component ids in the net   
    def get_id(self):
        return self.component_id
    
    def get_branch_ids(self):
        return self.branch_ids
        
    def get_component_ids(self):
        return self.component_ids
    
    def get_node_ids(self):
        return self.node_ids
    
    def get_mesh_ids(self):
        return self.mesh_ids
    
    def add_branch_id(self, brch_id):
        self.branch_ids.append(brch_id)
        
    def remove_branch_id(self, brch_id):
        self.branch_ids.remove(brch_id)
        
    def add_component_id(self, cmp_id):
        self.component_ids.append(cmp_id)
        
    def remove_component_id(self, cmp_id):
        self.component_ids.remove(cmp_id)
        
    def add_node_id(self, nd_id):
        self.node_ids.append(nd_id)
        
    def remove_node_id(self, nd_id):
        self.node_ids.remove(nd_id)
        
    def add_mesh_id(self, msh_id):
        self.mesh_ids.append(msh_id)
        
    def remove_mesh_id(self, msh_id):
        self.mesh_ids.remove(msh_id)
        
# Creates a new net with the given id and component ids
def add_net(id, brch_ids, cmp_ids, nd_ids, msh_ids=[]):
    return Net(id, brch_ids, cmp_ids, nd_ids, msh_ids)

