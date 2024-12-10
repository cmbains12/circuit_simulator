## Utils functions
# This file contains utility functions that are used in the main application. These functions are
# used to get the display resolution of the screen, get the last component id, and get the last
# branch id. The display resolution is used to set the size of the main window of the application.
# The last component id and the last branch id are used to generate unique ids for new components
# and branches. The functions are imported and used in the main window and other files in the
# application.

from PyQt5.QtWidgets import QDesktopWidget

from analysis.branch import add_branch

# Get the display resolution of the screen
def get_display_resolution(self):
        screen = QDesktopWidget().screenGeometry()
        self.display_width = screen.width()
        self.display_height = screen.height()

# Get the last component id from the list of components
def get_last_component_id(components):
        if len(components) == 0:
                return 0
        else:
                return components[-1].id

# Get the last branch id from the list of branches   
def get_last_net_id(nets):
        if len(nets) == 0:
                return 0
        else:
                return nets[-1].id

def get_last_branch_id(branches):
        if len(branches) == 0:
                return 0
        else:
                return branches[-1].id

def net_by_id(nets, id):
        for net in nets:
                if net.id == id:
                        return net
        return None

def branch_by_id(branches, id):
        for branch in branches:
                if branch.id == id:
                        return branch
        return None

def component_by_id(components, id):
        for component in components:
                if component.id == id:
                        return component
        return None

def node_by_id(nodes, id):
        for node in nodes:
                if node.id == id:
                        return node
        return None

def define_branches(branches, components, nodes):
        branches = []
        terminal_components = []
        internal_components = []
        
        
        
        for node in nodes:
                if len(node.component_ids) == 1:
                        node.net_type = 'terminal'
                elif len(node.component_ids) == 2:
                        node.net_type = 'internal'
                elif len(node.component_ids) > 2:
                        node.net_type = 'junction'

        for component in components:
                node_ids= component.get_node_ids()
                component.set_net_type('internal')
                
                for node_id in node_ids:
                        net_type = node_by_id(nodes,node_id).get_net_type()
                        
                        if net_type == 'junction' or net_type == 'terminal':
                                component.set_net_type('terminal')

                if component.get_net_type() == 'terminal':
                        terminal_components.append(component)
                        
                elif component.get_net_type() == 'internal':
                        internal_components.append(component)
                        
        while terminal_components:
                component = terminal_components[0]
                branch = [component]
                terminal_components.remove(component)
                
                next_component = component 
                
                next_flag = True
                while next_flag:
                        
                        next_flag = False
                        
                        adj_nodes = [node_by_id(nodes, node_id) for node_id in next_component.get_node_ids()]

                        for node in adj_nodes:
                                if not node in branch:
                                        branch.append(node)
                                
                                if node.get_net_type() == 'internal' and next_flag== False:
                                        
                                        node_comp_ids = node.get_component_ids().copy()
                                        comp_id_to_remove = next_component.get_id()
                                        node_comp_ids.remove(comp_id_to_remove)
                                        comp = component_by_id(components, node_comp_ids[0])
                                        
                                        if not comp in branch:
                                                
                                                next_component = comp
                                                branch.append(comp)
                                                next_flag = True
                                                if comp.get_net_type() == 'terminal':
                                                        terminal_components.remove(comp)
                                
                                        
                                                
                                        
                                
                                        
                branches.append(branch)     
                
        return branches   
                

                        
                        
