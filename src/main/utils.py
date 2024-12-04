
from PyQt5.QtWidgets import QDesktopWidget

from analysis.branch import branch_by_id, change_branch_id
from components.component import component_by_id

def get_display_resolution(self):
        screen = QDesktopWidget().screenGeometry()
        self.display_width = screen.width()
        self.display_height = screen.height()

def get_last_component_id(components):
    if len(components) == 0:
        return 0
    else:
        return components[-1].id
    
def get_last_branch_id(branches):
        if len(branches) == 0:
                return 0
        else:
                return branches[-1].id
        
