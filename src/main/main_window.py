## Main Window of the application
# This file contains the main window of the application. It contains the main window class 
# which is the main window of the application. It contains the canvas where the circuit is 
# drawn and the toolbars for adding components and other functionalities. It also contains the 
# dock widgets for displaying the list of components and branches in the circuit.

from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QDockWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from utils import get_display_resolution


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Simulator")
        
        # Get the display resolution
        self.display_width = None
        self.display_height = None
        self.window_width = 800
        self.window_height = 600
        get_display_resolution(self)
        
        # Set the window size to 200 pixels less than the display resolution
        self.window_width = self.display_width - 200
        self.window_height = self.display_height - 200

        # Set the window size and position
        self.setGeometry(100, 100, self.window_width, self.window_height)
        
        self.component_list = None
        self.node_list = None
        self.branch_list = None
        self.net_list = None
        self.mesh_list = None
        

        # Add the canvas and toolbars
        self.add_canvas()
        self.add_top_bar()
        self.add_right_bar()
        self.add_left_bar()
        
    # Add the top toolbar
    def add_top_bar(self):
        top_bar = QToolBar("Top Bar")
        self.addToolBar(Qt.TopToolBarArea, top_bar)

        # Add buttons to the toolbar to select the component type to be added to the canvas.
        # These are not functional yet, and the only components that can be added are conductors.
        button_names = ["Conductor", "Resistor", "Supply"]
        
        # Add the buttons to the toolbar
        for name in button_names:
            # Create an action for the button. An action is a user-triggered event, such as 
            # selecting a menu item, clicking a button, or pressing a key. 
            action = QAction(QIcon(), name, self)
            # Add the action to the toolbar. This creates a button with the given name on the 
            # toolbar.
            top_bar.addAction(action)
        
    # Add the left toolbar
    def add_left_bar(self):
        left_bar = QToolBar("Left Bar")
        self.addToolBar(Qt.LeftToolBarArea, left_bar)

        button_names = ["Set Branches", "Clear", "Button 3"]
        for name in button_names:
            action = QAction(QIcon(), name, self)
            
            if name == "Set Branches":
                action.triggered.connect(self.canvas.set_branches)
            left_bar.addAction(action)
            
            if name == "Clear":
                action.triggered.connect(self.canvas.clear)
                self.update_comp_list([])
                self.update_net_list([])
                self.update_mesh_list([])
                self.update_node_list([])
                self.update_branch_list([])

                
                
                
            
    # Add the right dock widget.  A dock widget is a window that can be docked in the main
    # window. It can be moved around, resized, and closed. It is typically used to display
    # additional information or controls.
    def add_right_bar(self):
        # Create a list widget to display the list of components
        self.component_list = QListWidget()
        self.component_list.setFixedWidth(300)
        
        # Create a list widget to display the list of nodes
        self.node_list = QListWidget()
        self.node_list.setFixedWidth(300)
        
        # Create a list widget to display the list of branches
        self.branch_list = QListWidget()
        self.branch_list.setFixedWidth(300)

        # Create a list widget to display the list of nets
        self.net_list = QListWidget()
        self.net_list.setFixedWidth(300)
        
        # Create a list widget to display the list of meshes 
        self.mesh_list = QListWidget()
        self.mesh_list.setFixedWidth(300)

        # Create a dock widget to display the list of components
        dock_widget_1 = QDockWidget("Components", self)
        dock_widget_1.setWidget(self.component_list)
        
        # Create a dock widget to display the list of nodes
        dock_widget_2 = QDockWidget("Nodes", self)
        dock_widget_2.setWidget(self.node_list)
        
        # Create a dock widget to display the list of branches
        dock_widget_3 = QDockWidget("Branches", self)
        dock_widget_3.setWidget(self.branch_list)

        # Create a dock widget to display the list of nets
        dock_widget_4 = QDockWidget("Nets", self)
        dock_widget_4.setWidget(self.net_list)
        
        # Create a dock widget to display the list of meshes
        dock_widget_5 = QDockWidget("Meshes", self)
        dock_widget_5.setWidget(self.mesh_list)
        
        # Add the dock widgets to the right side of the main window
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_1)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_2)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_3)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_4)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_5)



    # Add the canvas to the main window
    def add_canvas(self):
        from canvas import Canvas
        
        # Create the canvas
        self.canvas = Canvas(self, main_window=self)
        
        # Set the canvas as the central widget of the main window.
        self.setCentralWidget(self.canvas)

    # Update the list of components in the right dock widget
    def update_comp_list(self, component_ids = []):
        # Clear the list widget
        self.component_list.clear()
        # Add the component ids to the list widget
        self.component_list.addItems([str(comp_id) for comp_id in component_ids])

    # Update the list of nets in the right dock widget
    def update_net_list(self, net_ids = []):
        # Clear the list widget
        self.net_list.clear()
        # Add the net ids to the list widget
        self.net_list.addItems([str(net_id) for net_id in net_ids])
        
    # Update the list of meshes in the right dock widget
    def update_mesh_list(self, mesh_ids = []):
        # Clear the list widget
        self.mesh_list.clear()
        # Add the mesh ids to the list widget
        self.mesh_list.addItems([str(mesh_id) for mesh_id in mesh_ids])
        
    # Update the list of nodes in the right dock widget
    def update_node_list(self, node_ids = []):
        # Clear the list widget
        self.node_list.clear()
        # Add the node ids to the list widget
        self.node_list.addItems([str(node_id) for node_id in node_ids])
        
    # Update the list of branches in the right dock widget
    def update_branch_list(self, branch_ids = []):
        # Clear the list widget
        self.branch_list.clear()
        # Add the branch ids to the list widget
        self.branch_list.addItems([str(branch_id) for branch_id in branch_ids])
        
    






