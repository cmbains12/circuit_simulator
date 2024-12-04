## Utils functions
# This file contains utility functions that are used in the main application. These functions are
# used to get the display resolution of the screen, get the last component id, and get the last
# branch id. The display resolution is used to set the size of the main window of the application.
# The last component id and the last branch id are used to generate unique ids for new components
# and branches. The functions are imported and used in the main window and other files in the
# application.

from PyQt5.QtWidgets import QDesktopWidget

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
def get_last_branch_id(branches):
        if len(branches) == 0:
                return 0
        else:
                return branches[-1].id
        
