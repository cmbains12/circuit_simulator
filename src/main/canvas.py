
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

from components.component import add_component, add_node_id
from analysis.branch import create_branch
from utils import get_last_component_id, get_last_branch_id
from components.node import add_node, add_component_id




class Canvas(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setMinimumSize(400,400)
        self.components = []
        self.component_selection = 'Conductor'
        self.pen_color = QColor(Qt.black)
        self.pen_width = 2

        self.start_pos = None
        self.end_pos = None
        
        self.branches = []
        self.branch_selection = None

        self.nodes = []
        self.new_branch = True
        self.end_branch = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QColor(Qt.white))
        pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine)
        painter.setPen(pen)

        if self.start_pos and self.end_pos:
            painter.drawLine(self.start_pos, self.end_pos)
            painter.drawEllipse(self.start_pos, 5, 5)
            painter.drawEllipse(self.end_pos, 5, 5)

        for component in self.components:
            painter.drawLine(component.start_pos, component.end_pos)

        for node in self.nodes:
            painter.drawEllipse(node.pos, 5, 5)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        self.end_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()

            comp_id = get_last_component_id(self.components) + 1
            component = add_component(self.component_selection, comp_id, self.start_pos, self.end_pos)
            
            if self.new_branch:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.start_pos)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)

            if not self.end_branch:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.end_pos)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)

            self.components.append(component)

            self.start_pos = None
            self.end_pos = None

            if not self.branch_selection:
                branch_id = get_last_branch_id(self.branches) + 1
                new_branch = create_branch(branch_id, component)
                self.branches.append(new_branch)

            if self.main_window:
                self.main_window.add_component_to_list(component)
                self.main_window.add_branch_to_list(new_branch)



            self.update()





    

        

    