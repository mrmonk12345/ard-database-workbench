
"""Start the ARD Database graphical interface."""

import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Create the Qt application and display the main window."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
