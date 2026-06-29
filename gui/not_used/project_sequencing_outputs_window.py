from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from scripts.python.project_get_data import get_project_sequencing_outputs
from gui.ui_utils import create_table
class ProjectSequencingOutputsWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle("Sequencing Outputs")
        self.resize(500, 400)

        layout = QVBoxLayout()
        try:
            outputs = get_project_sequencing_outputs(self.project_id)

            layout.addWidget(QLabel(f"Sequencing Outputs table ({len(outputs)} rows)"))
            table = create_table(outputs)
            layout.addWidget(table)

        except Exception as e:
            layout.addWidget(QLabel(f"Error fetching samples: {e}"))

        layout.addWidget(QLabel("Sequencing Outputs table"))

        self.setLayout(layout)