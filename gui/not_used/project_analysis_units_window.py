from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

from scripts.python.project_get_data import get_project_analysis_units

from gui.ui_utils import create_table
class ProjectAnalysisUnitsWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id
        
        self.setWindowTitle("Analysis Units")
        self.resize(500, 400)

        layout = QVBoxLayout()
        try:
            analysis_units = get_project_analysis_units(self.project_id)

            layout.addWidget(QLabel(f"Analysis Units table ({len(analysis_units)} rows)"))
            table = create_table(analysis_units)
            layout.addWidget(table)
        except Exception as e:
            layout.addWidget(QLabel(f"Error fetching analysis units: {e}"))

        self.setLayout(layout)