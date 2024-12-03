
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
        self.setMouseTracking(True)
        self.setMinimumSize(400,400)
        self.components = []
        self.component_selection = 'Conductor'
        self.pen_color = QColor(Qt.black)
        self.pen_width = 2

        self.current_pos = None
        self.start_pos = None
        self.end_pos = None
        
        self.nearest_node = None
        self.snap_distance = 20
        
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
            
        if self.current_pos and not self.nearest_node:
            
            painter.setPen(QPen(QColor(Qt.red), 5))
            painter.drawEllipse(self.current_pos, 2, 2)
            
        if self.nearest_node:
            painter.setPen(QPen(QColor(Qt.red), 5))
            painter.drawEllipse(self.nearest_node.pos, 2, 2)
            


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.nearest_node = self.find_nearest_node(event.pos())
            if self.nearest_node:
                self.start_pos = self.nearest_node.pos
                self.new_branch = False
            else:
                self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        self.current_pos = event.pos()
        self.nearest_node = self.find_nearest_node(self.current_pos)
        if event.buttons() == Qt.LeftButton:
            self.end_pos = self.current_pos
            if self.nearest_node:
                self.end_pos = self.nearest_node.pos
            
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            nearest_node = self.find_nearest_node(self.end_pos)
            
            if nearest_node:
                self.end_pos = nearest_node.pos


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

            if not self.branch_selection:
                branch_id = get_last_branch_id(self.branches) + 1
                new_branch = create_branch(branch_id, component)
                self.branches.append(new_branch)

            if self.main_window:
                self.main_window.add_component_to_list(component)
                self.main_window.add_branch_to_list(new_branch)

            self.start_pos = None
            self.end_pos = None
            self.end_branch = False
            self.nearest_node = None
            self.update()

        

    def find_nearest_node(self, pos):
        nearest_node = None
        min_dist = float('inf')
        
        
        for node in self.nodes:
            try:
                dist = (node.pos - pos).manhattanLength()
            except:
                break
            if dist < min_dist and dist <= self.snap_distance:
                min_dist = dist
                nearest_node = node

        return nearest_node
        



    

        

    