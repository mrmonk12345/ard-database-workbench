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

from gui.project_samples_add_window import ProjectSamplesAddWindow
from gui.project_libraries_add_window import ProjectLibrariesAddWindow

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

        # Load counts once
        self.counts = self._load_counts()

        # --- Top section ---
        top = QHBoxLayout()
        top.addWidget(self._create_display_box("Sequencing Runs", self.counts["runs"]))
        top.addWidget(self._create_display_box("Amplicon Types", self.counts["amplicon"]))
        layout.addLayout(top)

        # Combined button
        btn = QPushButton("View Sequencing Runs & Amplicon Types")
        btn.clicked.connect(self.open_runs_amplicon)
        layout.addWidget(btn)

        # --- Remaining sections ---
        layout.addWidget(self._create_action_box("Samples", self.counts["samples"], ProjectSamplesWindow, None))
        layout.addWidget(self._create_action_box("Sequencing Outputs", self.counts["outputs"], ProjectSequencingOutputsWindow, None))
        layout.addWidget(self._create_action_box("Libraries", self.counts["libraries"], ProjectLibrariesWindow, None))
        layout.addWidget(self._create_action_box("Analysis Units", self.counts["analysis_units"], ProjectAnalysisUnitsWindow, None))

        self.setLayout(layout)

    # =====================
    # Data
    # =====================

    def _load_counts(self):
        return {
            "runs": get_project_sequencing_runs_count(self.project_id),
            "amplicon": get_project_amplicon_types_count(self.project_id),
            "samples": get_project_samples_count(self.project_id),
            "outputs": get_project_sequencing_outputs_count(self.project_id),
            "libraries": get_project_libraries_count(self.project_id),
            "analysis_units": get_project_analysis_units_count(self.project_id),
        }

    # =====================
    # UI helpers
    # =====================

    def _create_count_label(self, count):
        lbl = QLabel(str(count))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        return lbl

    def _create_display_box(self, title, count):
        box = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addWidget(self._create_count_label(count))
        box.setLayout(layout)

        return box

    def _create_action_box(self, title, count, view_cls, add_cls):
        box = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addWidget(self._create_count_label(count))

        # Button row
        btn_layout = QHBoxLayout()

        # ✅ View button
        view_btn = QPushButton(f"View {title}")
        view_btn.clicked.connect(lambda _, cls=view_cls: self.open_window(cls))

        
        # ✅ Add button
        add_btn = QPushButton(f"Add {title}")
        add_btn.clicked.connect(lambda _, cls=add_cls: self.open_window(cls))

        btn_layout.addWidget(view_btn)
        if add_cls:
            btn_layout.addWidget(add_btn)

        layout.addLayout(btn_layout)
        box.setLayout(layout)

        return box

    # =====================
    # Actions
    # =====================

    def open_runs_amplicon(self):
        self.window = ProjectAmpliconRunsWindow(self, project_id=self.project_id)
        self.window.show()

    def open_window(self, cls):
        self.window = cls(self, project_id=self.project_id)
        self.window.show()