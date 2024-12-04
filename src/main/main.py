## This file is the entry point of the application. It creates the main window and starts the 
# application. The main window contains the canvas where the circuit is drawn and the toolbars
# for adding components and other functionalities. It also contains the dock widgets for 
# displaying the list of components and branches in the circuit. The main window is created using
# the PyQt5 library.

import sys
import os

# Add the parent directory to the sys.path so that the modules in the parent directory can be
# imported.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
