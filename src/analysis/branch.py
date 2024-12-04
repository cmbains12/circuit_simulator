


class Branch():
    def __init__(self, id, component_ids):
        self.id = id
        self.component_ids = []
        self.component_ids.append(component_ids)
        
    def get_ids(self):
        return self.component_ids


def create_branch(id, component_ids):
    return Branch(id, component_ids)

def branch_by_id(branches, branch_id):
    for branch in branches:
        if branch.id == branch_id:
            return branch
    return None   
    

def change_branch_id(branch, new_id):
    branch.id = new_id
    
    
def add_component_id(branch, component_id):
    branch.component_ids.append(component_id)






