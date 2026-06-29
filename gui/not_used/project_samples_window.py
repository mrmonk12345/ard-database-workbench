from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from scripts.python.project_get_data import get_project_samples

from gui.ui_utils import create_table
class ProjectSamplesWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle("Samples")
        self.resize(500, 400)

        layout = QVBoxLayout()

        try:
            samples = get_project_samples(self.project_id)
            
            layout.addWidget(QLabel(f"Samples table ({len(samples)} rows)"))
            table = create_table(samples)
            layout.addWidget(table)

        except Exception as e:
            layout.addWidget(QLabel(f"Error fetching samples: {e}"))

        self.setLayout(layout)