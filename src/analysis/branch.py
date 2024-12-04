## Branch class and functions
# Branch class is used to store the components that are connected to each other.
# Each branch has an id and a list of component ids.


class Branch():
    def __init__(self, id, component_ids):
        self.id = id
        self.component_ids = []
        self.component_ids.append(component_ids)
    
    # Returns the list of component ids in the branch   
    def get_ids(self):
        return self.component_ids

# Creates a new branch with the given id and component ids
def create_branch(id, component_ids):
    return Branch(id, component_ids)

# Returns the branch with the given id from the list of branches
def branch_by_id(branches, branch_id):
    for branch in branches:
        if branch.id == branch_id:
            return branch
    return None   
    
# Changes the id of the given branch to the new id
def change_branch_id(branch, new_id):
    branch.id = new_id
    
# Adds a new component id to the given branch   
def add_component_id(branch, component_id):
    branch.component_ids.append(component_id)






