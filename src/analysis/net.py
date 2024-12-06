## Net class and functions
# Net class is used to store the components that are connected to each other.
# Each net has an id and a list of component ids.


class Net():
    def __init__(self, id, component_ids):
        self.id = id
        self.component_ids = []
        self.component_ids.append(component_ids)
    
    # Returns the list of component ids in the net   
    def get_ids(self):
        return self.component_ids

# Creates a new net with the given id and component ids
def create_net(id, component_ids):
    return Net(id, component_ids)

# Returns the net with the given id from the list of nets
def net_by_id(nets, net_id):
    for net in nets:
        if net.id == net_id:
            return net
    return None   
    
# Changes the id of the given net to the new id
def change_net_id(net, new_id):
    net.id = new_id
    
# Adds a new component id to the given net   
def add_component_id(net, component_id):
    net.component_ids.append(component_id)






