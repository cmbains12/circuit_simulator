


class Branch ():
    def __init__(self, id, nt_id, cmpt_ids, nd_ids, msh_ids = []):
        self.id = id
        self.net_id = nt_id
        self.component_ids = []
        self.component_ids.append(cmpt_ids)
        self.node_ids = nd_ids
        self.mesh_ids = msh_ids
        
    def get_id(self):
        return self.id
    
    def get_net_id(self):
        return self.net_id
    
    def get_component_ids(self):
        return self.component_ids
    
    def get_node_ids(self):
        return self.node_ids
    
    def get_mesh_ids(self):
        return self.mesh_ids
    
    def change_branch_id(self, new_id):
        self.id = new_id
        
    def change_net_id(self, new_id):
        self.net_id = new_id
        
    def add_component_id(self, cmpt_id):
        self.component_ids.append(cmpt_id)
        
    def remove_component_id(self, cmpt_id):
        self.component_ids.remove(cmpt_id)
        
    def add_node_id(self, nd_id):
        self.node_ids.append(nd_id)
        
    def remove_node_id(self, nd_id):
        self.node_ids.remove(nd_id)
        
    def add_mesh_id(self, msh_id):
        self.mesh_ids.append(msh_id)
        
    def remove_mesh_id(self, msh_id):
        self.mesh_ids.remove(msh_id)
        
def add_branch(id, nt_id, cmpt_ids, nd_ids, msh_ids=[]):
    return Branch(id, nt_id, cmpt_ids, nd_ids, msh_ids)


        