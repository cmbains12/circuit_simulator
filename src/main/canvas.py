## Canvas class definition and methods
# The Canvas class is a QWidget that is used to draw the electrical circuit. It has a list of
# components, a component selection, a pen color, a pen width, the current position of the mouse,
# the start and end positions of the component being drawn, the nearest node to the mouse cursor,
# a snap distance, a list of nets, the id of the selected net, the id of the other net
# that the component is to be connected to, a list of nodes, and flags to indicate if a new net is
# being created or if the component is connecting to an existing node. The Canvas class has
# methods to draw the components, nodes, handle mouse events, find the nearest node
# to the mouse cursor, and merge nets.


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

from components.component import add_component, Component
from analysis.net import add_net
from analysis.mesh import add_mesh
from analysis.branch import add_branch
from utils import get_last_component_id, get_last_net_id, net_by_id, get_last_branch_id, branch_by_id, component_by_id, node_by_id, define_branches
from components.node import add_node, Node

class Canvas(QWidget):
    def __init__(self, parent=None, main_window=None):
        # Initialize the QWidget
        super().__init__(parent)
        # Set the main window reference
        self.main_window = main_window
        # Enable mouse tracking to get mouse move events even when no button is pressed
        self.setMouseTracking(True)
        # Set the minimum size of the canvas
        self.setMinimumSize(400,400)
        self.components = []
        # For now, only conductor components are supported
        self.component_selection = 'Conductor'
        
        
        # Set the default pen color and width
        self.pen_color = QColor(Qt.black)
        self.pen_width = 2

        # Initialize the positions of the component being drawn and the nearest node
        self.current_pos = None
        self.start_pos = None
        self.end_pos = None
        self.nearest_node = None
        
        # Set the snap distance for snapping to nodes
        self.snap_distance = 20
        
        # Initialize the list of nets and the net selection id and other net id
        self.nets = []
        self.net_selection_id = 0
        #self.other_net_id = None
        
        # Initialize the list of branches and the branch selection id and other branch id
        self.branches = []
        self.branch_selection_id = 0
        #self.other_branch_id = None
                
        # Initialize the list of meshes and the mesh selection id and other mesh id
        self.meshes = []
        #self.mesh_selection_id = 0
        #self.other_mesh_id = None
        
        # Initialize a variable that stores the draw/select mode
        self.draw_mode = True
        
        # Initialize the id of the node or component that is selected by the cursor
        self.selected_type = None
        self.selected_id = None
        

        # Initialize the list of nodes
        self.nodes = []
        
        self.node_1_id = None
        self.node_2_id = None
        
        # Flags to indicate if a new net is being created or if the component is connecting 
        # to an existing node
        self.new_node_1 = True
        self.new_node_2 = True
        
        #self.new_branch = False

    # Draws the components and nodes on the canvas
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QColor(Qt.white))
        pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine)
        painter.setPen(pen)
        
        # Preview of the component being drawn
        if self.start_pos and self.end_pos:
            painter.drawLine(self.start_pos, self.end_pos)
            painter.drawEllipse(self.start_pos, 5, 5)
            painter.drawEllipse(self.end_pos, 5, 5)

        # Draw the components and nodes
        for component in self.components:
            painter.drawLine(component.start_pos, component.end_pos)

        for node in self.nodes:
            painter.drawEllipse(node.pos, 5, 5)
        
        # Draw the current position of the mouse cursor if not snapped to a node    
        if self.current_pos and not self.nearest_node:
            painter.setPen(QPen(QColor(Qt.red), 5))
            painter.drawEllipse(self.current_pos, 2, 2)
            
        # Show the nearest node to the mouse cursor if snapped 
        if self.nearest_node:
            painter.setPen(QPen(QColor(Qt.red), 5))
            painter.drawEllipse(self.nearest_node.pos, 2, 2)
            
    # Handles mouse press events
    def mousePressEvent(self, event):
        
        # Left mouse button press
        if event.button() == Qt.LeftButton and self.draw_mode:
            
            # Find the nearest node to the mouse cursor and snap to it
            self.nearest_node = self.find_nearest_node(event.pos())
            
            # If a node is snapped to, set the start position to the node position,
            # set the net selection id to the node's net id, 
            # and set new net flag to False
            if self.nearest_node:
                
                #self.net_selection_id = self.nearest_node.net_id
                self.start_pos = self.nearest_node.pos
                self.new_node_1 = False
                self.node_1_id = self.nearest_node.get_id()
                
                #self.net_selection_id = self.nearest_node.get_net_id()
                #self.branch_selection_id = self.nearest_node.get_branch_id()
                
                #if len(self.nearest_node.get_component_ids()) == 1:
                    #self.new_branch = False
                    
                #else:
                    #self.new_branch = True

            # If no node is snapped to, set the start position to the mouse cursor position,
            # set the net selection id to the last net id + 1, 
            # and keep the new net flag as True
            else:
                self.start_pos = event.pos()
                
                
            # To preview the component being drawn, set the end position to the mouse cursor position
            self.end_pos = event.pos()
            
            # Update the canvas
            self.update()
            
        elif event.button() == Qt.LeftButton and not self.draw_mode:
            pass

    # Handles mouse move events
    def mouseMoveEvent(self, event):
        
        # Update the current position of the mouse cursor
        self.current_pos = event.pos()
        
        # Find the nearest node to the mouse cursor and snap to it if within the snap distance
        self.nearest_node = self.find_nearest_node(self.current_pos)
        
        
        # If the left mouse button is pressed, update the end position of the component being drawn
        if event.buttons() == Qt.LeftButton:
            
            self.end_pos = self.current_pos
            if self.nearest_node:
                
                self.end_pos = self.nearest_node.pos
        self.update()
        
    # Handles mouse release events
    def mouseReleaseEvent(self, event):
        
        # If the left mouse button is released
        if event.button() == Qt.LeftButton:
            
            # If the end position is snapped to a node, set the end position to the node position
            # and set the end net flag to True if the net selection id is not the same as 
            # the node's net id. If the end position is not snapped to a node, set the end 
            # position to the mouse cursor position.
            self.nearest_node = self.find_nearest_node(self.end_pos)
            #net = None
            #branch = None
            if self.nearest_node:
                self.end_pos = self.nearest_node.pos
                self.new_node_2 = False
                self.node_2_id = self.nearest_node.get_id()
            #    self.other_net_id = self.nearest_node.net_id
            #    self.other_branch_id = self.nearest_node.get_branch_id()
                
                
            else:
                
                self.end_pos = event.pos()
                
            
            
            #if self.new_node_1 and self.new_node_2:
            #    self.new_branch = True
            #    self.net_selection_id = get_last_net_id(self.nets) + 1
            #    net = add_net(self.net_selection_id, self.branch_selection_id, cmp_ids = [], nd_ids=[])
            #    self.nets.append(net)
            #    self.main_window.update_net_list([net.id for net in self.nets])
                # Create a new component with an id that is one more than the last component id,
            
            #if self.new_branch:
            #    self.branch_selection_id = get_last_branch_id(self.branches) + 1
            #    branch = add_branch(self.branch_selection_id, self.net_selection_id, cmp_ids = [], nd_ids = []) 
            #    self.branches.append(branch)
            #    self.main_window.update_branch_list([branch.id for branch in self.branches])
            #    self.new_branch = False            
            # the start and end positions, the net selection id, and the other net id if
            # the end position is snapped to a node.
            comp_id = get_last_component_id(self.components) + 1    
            component = add_component(self.component_selection, comp_id, self.branch_selection_id, self.net_selection_id, self.start_pos, self.end_pos, nd_ids = [])
            #type, id, brch_id, nt_id, st_pos, nd_pos, msh_ids=[], nt_type=None, nd_ids=[]
            #branch_by_id(self.branches, self.branch_selection_id).add_component_id(comp_id)
            #net_by_id(self.nets, self.net_selection_id).add_component_id(comp_id)

                
            # If the start position is not snapped to a node, create a new node with an id that 
            # is one more than the last node id, the start position, and the net selection id.
            if self.new_node_1:
                
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id,self.branch_selection_id, self.net_selection_id, cmp_ids = comp_id, pos = self.start_pos)
                self.nodes.append(node)
                component.add_node_id(node_id)
            else:
                node_by_id(self.nodes, self.node_1_id).add_component_id(comp_id)
                component.add_node_id(self.node_1_id)
                
                
            #    net_by_id(self.nets, self.net_selection_id).add_node_id(node_id)
            #    branch_by_id(self.branches, self.branch_selection_id).add_node_id(node_id)
                
            

                
               
            # If the end position is not snapped to a node, create a new node with an id that
            # is one more than the last node id, the end position, and the net selection id.
            if self.new_node_2:
                
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.branch_selection_id, self.net_selection_id, cmp_ids = comp_id, pos = self.end_pos)
                self.nodes.append(node)
                component.add_node_id(node_id)
                
            else:
                node_by_id(self.nodes, self.node_2_id).add_component_id(comp_id)
                component.add_node_id(self.node_2_id)
                
            #    net_by_id(self.nets, self.net_selection_id).add_node_id(node_id)
            #    branch_by_id(self.branches, self.branch_selection_id).add_node_id(node_id)

            # Add the component to the list of components
            self.components.append(component)
            
            # If a new net is being created, create a new net with an id that is one more
            # than the last net id contains the new component id. Add the net to the list 
            # of nets and update the net list in the main window.            
            
                
            
            # If the end position is snapped to a node, set the other net id to the node's 
            # net id.     
            #if not self.new_node_2:
                
                
                # If the net selection id is not the same as the other net id, merge the
                # nets.
                #if self.net_selection_id != self.other_net_id:
                    #self.merge_nets(self.net_selection_id, self.other_net_id)
                    
                #if self.branch_selection_id != self.other_branch_id:
                #    self.merge_branches(self.branch_selection_id, self.other_branch_id)

            # Update the component and net lists in the main window
            self.main_window.update_net_list([net.id for net in self.nets])
            self.main_window.update_comp_list([comp.id for comp in self.components])
   
            # Reset the start and end positions, the nearest node, and the flags
            self.start_pos = None
            self.end_pos = None
            self.new_node_2 = True
            self.nearest_node = None
            self.new_node_1 = True
            self.update()
            
            

            

    # Merges two nets by removing one of the nets and changing the net id of the
    # components and nodes that belong to the removed net to the other net id.
    def merge_nets(self, net_id_1, net_id_2):
        
        net1_length = len(net_by_id(self.nets, net_id_1).component_ids)
        net2_length = len(net_by_id(self.nets, net_id_2).component_ids)
        
        net_to_remove = None
        net_to_keep = None
        
        if net1_length > net2_length:
            net_to_remove = net_id_2
            net_to_keep = net_id_1
            
        elif net1_length < net2_length:
            net_to_remove = net_id_1
            net_to_keep = net_id_2
            
        elif net1_length == net2_length:
            if net_id_1 < net_id_2:
                net_to_remove = net_id_2
                net_to_keep = net_id_1
            elif net_id_1 > net_id_2:
                net_to_remove = net_id_1
                net_to_keep = net_id_2
                        
       
        net_by_id(self.nets, net_to_keep).add_component_id([comp.id for comp in self.components if comp.net_id == net_to_remove])
        
        #for component in self.components:
        #    if component.net_id == net_to_remove:
        #        component.change_net_id(net_to_keep)
                
        
        #component_by_id(self.components, [id for id in net_by_id(self.nets, net_to_remove).get_component_ids()]).change_net_id(net_to_keep)
        
        for component in self.components:
            if component.net_id == net_to_remove:
                component.change_net_id(net_to_keep)
                
        for node in self.nodes:
            if node.net_id == net_to_remove:
                node.change_net_id(net_to_keep)
        
        #node_by_id(self.nodes, [node_id for node_id in net_by_id(self.nets, net_to_remove).get_node_ids()]).change_net_id(net_to_keep)
           
        self.nets.remove(net_by_id(self.nets, net_to_remove))
        
    def merge_branches(self, branch_id_1, branch_id_2):
            
        branch1_length = len(branch_by_id(self.branches, branch_id_1).component_ids)
        branch2_length = len(branch_by_id(self.branches, branch_id_2).component_ids)
            
        branch_to_remove = None
        branch_to_keep = None
            
        if branch1_length > branch2_length:
                branch_to_remove = branch_id_2
                branch_to_keep = branch_id_1
                
        elif branch1_length < branch2_length:
                branch_to_remove = branch_id_1
                branch_to_keep = branch_id_2
                
        elif branch1_length == branch2_length:
            if branch_id_1 < branch_id_2:
                branch_to_remove = branch_id_2
                branch_to_keep = branch_id_1
            elif branch_id_1 > branch_id_2:
                branch_to_remove = branch_id_1
                branch_to_keep = branch_id_2
                            
        branch_by_id(self.branches, branch_to_keep).add_component_id([comp.id for comp in self.components if comp.branch_id == branch_to_remove])
            
        for component in self.components:
            if component.get_branch_id() == branch_to_remove:
                component.change_branch_id(branch_to_keep)
                    
        for node in self.nodes:
            if node.get_branch_id() == branch_to_remove:
                node.change_branch_id(branch_to_keep)
                
        self.branches.remove(branch_by_id(self.branches, branch_to_remove))
    
    # Finds the nearest node to a given position within the snap distance
    def find_nearest_node(self, pos):
        nearest_node = None
        # Initialize the minimum distance to infinity
        min_dist = float('inf')
        # Iterate through the list of nodes and find the node with the minimum distance
        for node in self.nodes:
            
            # Calculate the distance between the node position and the given position
            try:
                dist = (node.pos - pos).manhattanLength()
                
            # If the distance cannot be calculated, break the loop
            except:
                break
            
            # If the distance is less than the minimum distance and within the snap distance,
            # update the minimum distance and the nearest node
            if dist < min_dist and dist <= self.snap_distance:
                min_dist = dist
                nearest_node = node
                
        # Return the nearest node
        return nearest_node

    def set_branches(self):
        self.branches = []
        branch_list = define_branches(self.branches, self.components, self.nodes)
            
        for branch in branch_list:
            nodes = []
            components = []
            self.branch_selection_id = get_last_branch_id(self.branches) + 1
            for item in branch:
                if isinstance(item, Node):
                    nodes.append(item.get_id())
                        
                elif isinstance(item, Component):
                    components.append(item.get_id())
                
            new_branch = add_branch(self.branch_selection_id, self.net_selection_id, components, nodes )

            self.branches.append(new_branch)
            self.main_window.update_branch_list([branch.id for branch in self.branches])

    






