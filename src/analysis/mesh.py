## Mesh class and functions


class Mesh():
    def __init__(self, id, nt_id, brch_ids, cmp_ids, nd_ids):
        self.id = id
        self.net_id = nt_id
        self.branch_ids = brch_ids
        self.component_ids = cmp_ids
        self.node_ids = nd_ids
    
    # Returns the list of component ids in the net   
    def get_id(self):
        return self.id
    
    def get_net_id(self):
        return self.net_id
    
    def get_branch_ids(self):
        return self.branch_ids
    
    def get_component_ids(self):
        return self.component_ids
    
    def get_node_ids(self):
        return self.node_ids
    
    def change_net_id(self, new_id):
        self.net_id = new_id
        
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
        
def add_mesh(id, nt_id, brch_ids, cmp_ids, nd_ids):
    return Mesh(id, nt_id, brch_ids, cmp_ids, nd_ids)

