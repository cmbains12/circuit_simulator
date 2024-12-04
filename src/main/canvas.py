
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

from components.component import add_component, add_node_id
from analysis.branch import create_branch, branch_by_id
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
        self.branch_selection_id = None
        self.other_branch_id = None

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
                self.branch_selection_id = self.nearest_node.branch_id
                self.start_pos = self.nearest_node.pos
                self.new_branch = False
            else:
                self.start_pos = event.pos()
                self.branch_selection_id = get_last_branch_id(self.branches) + 1
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
            self.nearest_node = self.find_nearest_node(self.end_pos)
            self.other_branch_id = None
            if self.nearest_node:
                self.end_pos = self.nearest_node.pos
                if self.branch_selection_id != self.nearest_node.branch_id:
                    self.end_branch = True
                
            comp_id = get_last_component_id(self.components) + 1
            component = add_component(self.component_selection, comp_id, self.start_pos, self.end_pos, branch_id=self.branch_selection_id)
            
            if self.new_branch:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.start_pos, self.branch_selection_id)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)

            if not self.end_branch:
                node_id = get_last_component_id(self.nodes) + 1
                node = add_node(node_id, self.end_pos, self.branch_selection_id)
                add_component_id(node, comp_id)
                self.nodes.append(node)
                add_node_id(component, node_id)

            self.components.append(component)

            if self.new_branch:
                branch_id = get_last_branch_id(self.branches) + 1
                branch = create_branch(branch_id, comp_id)
                self.branches.append(branch)
                self.branch_selection_id = branch_id
                self.main_window.update_branch_list([br.id for br in self.branches])
                
            if self.end_branch:
                self.other_branch_id = self.nearest_node.branch_id
                
                if self.branch_selection_id != self.other_branch_id:
                    self.merge_branches(self.branch_selection_id, self.other_branch_id)

            self.main_window.update_branch_list([br.id for br in self.branches])
            self.main_window.update_comp_list([comp.id for comp in self.components])
   
            
            self.start_pos = None
            self.end_pos = None
            self.end_branch = False
            self.nearest_node = None
            self.new_branch = True
            self.update()

    def merge_branches(self, branch_id_1, branch_id_2):
        branch1_length = len(branch_by_id(self.branches, branch_id_1).component_ids)
        branch2_length = len(branch_by_id(self.branches, branch_id_2).component_ids)
        
        if branch1_length > branch2_length:
            self.branches.remove(branch_by_id(self.branches, branch_id_2))
            for component in self.components:
                if component.branch_id == branch_id_2:
                    component.change_branch(branch_id_1)
            for node in self.nodes:
                if node.branch_id == branch_id_2:
                    node.change_branch(branch_id_1)
        elif branch1_length < branch2_length:
            self.branches.remove(branch_by_id(self.branches, branch_id_1))
            for component in self.components:
                if component.branch_id == branch_id_1:
                    component.change_branch(branch_id_2)
            for node in self.nodes:
                if node.branch_id == branch_id_1:
                    node.change_branch(branch_id_2)
        else:
            if branch_id_1 < branch_id_2:
                self.branches.remove(branch_by_id(self.branches, branch_id_2))
                for component in self.components:
                    if component.branch_id == branch_id_2:
                        component.change_branch(branch_id_1)
                for node in self.nodes:
                    if node.branch_id == branch_id_2:
                        node.change_branch(branch_id_1)
            else:
                self.branches.remove(branch_by_id(self.branches, branch_id_1))
                for component in self.components:
                    if component.branch_id == branch_id_1:
                        component.change_branch(branch_id_2)
                for node in self.nodes:
                    if node.branch_id == branch_id_1:
                        node.change_branch(branch_id_2)

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
        



    

        

    