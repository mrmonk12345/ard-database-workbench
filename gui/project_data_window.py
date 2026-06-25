from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt

from gui.project_amplicon_runs_window import ProjectAmpliconRunsWindow
from gui.project_samples_window import ProjectSamplesWindow
from gui.project_sequencing_outputs_window import ProjectSequencingOutputsWindow
from gui.project_libraries_window import ProjectLibrariesWindow
from gui.project_analysis_units_window import ProjectAnalysisUnitsWindow

from scripts.python.project_get_data import (
    get_project_sequencing_runs_count,
    get_project_amplicon_types_count,
    get_project_samples_count,
    get_project_sequencing_outputs_count,
    get_project_libraries_count,
    get_project_analysis_units_count
)

class ProjectDataWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle(f"Project Data - {self.project_id}")
        self.resize(500, 700)

        layout = QVBoxLayout()

        # ✅ TOP SIDE-BY-SIDE
        top = QHBoxLayout()
        top.addWidget(self.display_box("Sequencing Runs", str(get_project_sequencing_runs_count(self.project_id))))
        top.addWidget(self.display_box("Amplicon Types", str(get_project_amplicon_types_count(self.project_id))))
        layout.addLayout(top)

        # ✅ ONE BUTTON FOR BOTH
        btn = QPushButton("View Sequencing Runs & Amplicon Types")
        btn.clicked.connect(self.open_runs_amplicon)
        layout.addWidget(btn)

        # ✅ BELOW (individual)
        layout.addWidget(self.box("Samples", str(get_project_samples_count(self.project_id)), ProjectSamplesWindow))
        layout.addWidget(self.box("Sequencing Outputs", str(get_project_sequencing_outputs_count(self.project_id)), ProjectSequencingOutputsWindow))
        layout.addWidget(self.box("Libraries", str(get_project_libraries_count(self.project_id)), ProjectLibrariesWindow))
        layout.addWidget(self.box("Analysis Units", str(get_project_analysis_units_count(self.project_id)), ProjectAnalysisUnitsWindow))

        self.setLayout(layout)

    def display_box(self, title, count):
        box = QGroupBox(title)
        l = QVBoxLayout()

        lbl = QLabel(count)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold;")

        l.addWidget(lbl)
        box.setLayout(l)

        return box

    def box(self, title, count, window_class):
        box = QGroupBox(title)
        l = QVBoxLayout()

        lbl = QLabel(count)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold;")

        btn = QPushButton(f"Open {title}")
        btn.clicked.connect(lambda: self.open_window(window_class))

        l.addWidget(lbl)
        l.addWidget(btn)
        box.setLayout(l)

        return box

    def open_runs_amplicon(self):
        self.window = ProjectAmpliconRunsWindow(self, project_id=self.project_id)
        self.window.show()

    def open_window(self, cls):
        self.window = cls(self, project_id=self.project_id)
        self.window.show()
