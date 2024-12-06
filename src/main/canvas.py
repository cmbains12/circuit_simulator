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

from components.component import add_component, add_node_id
from analysis.net import create_net, net_by_id
from utils import get_last_component_id, get_last_net_id
from components.node import add_node, add_component_id

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
        self.net_selection_id = None
        self.other_net_id = None
        
        # Initialize a variable that stores the draw/select mode
        self.draw_mode = True
        
        # Initialize the id of the node or component that is selected by the cursor
        self.selected_type = None
        self.selected_id = None
        

        # Initialize the list of nodes
        self.nodes = []
        
        # Flags to indicate if a new net is being created or if the component is connecting 
        # to an existing node
        self.new_net = True
        self.end_net = False

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
                self.net_selection_id = self.nearest_node.net_id
                self.start_pos = self.nearest_node.pos
                self.new_net = False
            # If no node is snapped to, set the start position to the mouse cursor position,
            # set the net selection id to the last net id + 1, 
            # and keep the new net flag as True
            else:
                self.start_pos = event.pos()
                self.net_selection_id = get_last_net_id(self.nets) + 1
                
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
            self.other_net_id = None
            if self.nearest_node:
                self.end_pos = self.nearest_node.pos
                if self.net_selection_id != self.nearest_node.net_id:
                    self.end_net = True
            else:
                self.end_pos = event.pos()
            
            # Create a new component with an id that is one more than the last component id,
            # the start and end positions, the net selection id, and the other net id if
            # the end position is snapped to a node.
            
            comp_id = get_last_component_id(self.components) + 1    
            component = add_component(self.component_selection, comp_id, self.start_pos, self.end_pos, net_id=self.net_selection_id)
            
            # If the start position is not snapped to a node, create a new node with an id that 
            # is one more than the last node id, the start position, and the net selection id.
            if self.new_net:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.start_pos, self.net_selection_id)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)
                
            # If the end position is not snapped to a node, create a new node with an id that
            # is one more than the last node id, the end position, and the net selection id.
            if not self.end_net:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.end_pos, self.net_selection_id)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)

            # Add the component to the list of components
            self.components.append(component)
            
            

            # If a new net is being created, create a new net with an id that is one more
            # than the last net id contains the new component id. Add the net to the list 
            # of nets and update the net list in the main window.            
            if self.new_net:
                net_id = get_last_net_id(self.nets) + 1
                net = create_net(net_id, comp_id)
                self.nets.append(net)
                self.net_selection_id = net_id
                self.main_window.update_net_list([net.id for net in self.nets])
                
            # Add the new component id to the list of component ids in the net
            net_by_id(self.nets, component.net_id).component_ids.append(component.id)
            
            # If the end position is snapped to a node, set the other net id to the node's 
            # net id.     
            if self.end_net:
                self.other_net_id = self.nearest_node.net_id
                
                # If the net selection id is not the same as the other net id, merge the
                # nets.
                
                if self.net_selection_id != self.other_net_id:
                    self.merge_nets(self.net_selection_id, self.other_net_id)

            # Update the component and net lists in the main window
            self.main_window.update_net_list([net.id for net in self.nets])
            self.main_window.update_comp_list([comp.id for comp in self.components])
   
            # Reset the start and end positions, the nearest node, and the flags
            self.start_pos = None
            self.end_pos = None
            self.end_net = False
            self.nearest_node = None
            self.new_net = True
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
                        
        for net in self.nets:
            if net.id == net_to_keep:
                net.component_ids.append([comp.id for comp in self.components if comp.net_id == net_to_remove])    
        
        for component in self.components:
            if component.net_id == net_to_remove:
                component.change_net(net_to_keep)
                
        for node in self.nodes:
            if node.net_id == net_to_remove:
                node.change_net(net_to_keep)
            
        self.nets.remove(net_by_id(self.nets, net_to_remove))
    
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








