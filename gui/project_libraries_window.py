from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from scripts.python.project_get_data import get_project_libraries

from gui.ui_utils import create_table
class ProjectLibrariesWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle("Libraries")
        self.resize(500, 400)

        layout = QVBoxLayout()
        
        try:
            libraries = get_project_libraries(self.project_id)

            layout.addWidget(QLabel(f"Libraries table ({len(libraries)} rows)"))
            table = create_table(libraries)
            layout.addWidget(table)
        except Exception as e:
            layout.addWidget(QLabel(f"Error fetching libraries: {e}"))

        self.setLayout(layout)