from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QDockWidget, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


from utils import get_display_resolution

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Simulator")
        self.display_width = None
        self.display_height = None
        self.window_width = 800
        self.window_height = 600

        get_display_resolution(self)
        self.window_width = self.display_width - 200
        self.window_height = self.display_height - 200

        self.setGeometry(100, 100, self.window_width, self.window_height)

        self.add_canvas()
        self.add_top_bar()
        self.add_left_bar()
        self.add_right_bar()
        

    def add_top_bar(self):
        top_bar = QToolBar("Top Bar")
        self.addToolBar(Qt.TopToolBarArea, top_bar)

        button_names = ["Conductor", "Resistor", "Supply"]
        for name in button_names:
            action = QAction(QIcon(), name, self)
            top_bar.addAction(action)
        

    def add_left_bar(self):
        left_bar = QToolBar("Left Bar")
        self.addToolBar(Qt.LeftToolBarArea, left_bar)

        button_names = ["Button 1", "Button 2", "Button 3"]
        for name in button_names:
            action = QAction(QIcon(), name, self)
            left_bar.addAction(action)
            

    def add_right_bar(self):
        self.component_list = QListWidget()
        self.component_list.setFixedWidth(300)



        self.branch_list = QListWidget()
        self.branch_list.setFixedWidth(300)

        dock_widget_1 = QDockWidget("Components", self)
        dock_widget_1.setWidget(self.component_list)

        dock_widget_2 = QDockWidget("Branches", self)
        dock_widget_2.setWidget(self.branch_list)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_1)
        self.addDockWidget(Qt.RightDockWidgetArea, dock_widget_2)




    def add_canvas(self):
        from canvas import Canvas
        self.canvas = Canvas(self, main_window=self)
        self.setCentralWidget(self.canvas)


    def update_comp_list(self, component_ids):
        self.component_list.clear()
        self.component_list.addItems([str(comp_id) for comp_id in component_ids])

    def update_branch_list(self, branch_ids):
        self.branch_list.clear()
        self.branch_list.addItems([str(branch_id) for branch_id in branch_ids])






