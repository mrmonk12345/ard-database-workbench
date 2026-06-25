from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTabWidget,
    QWidget, QTableWidget, QTableWidgetItem
)

from scripts.python.project_get_data import (
    get_project_sequencing_runs,
    get_project_amplicon_types
)

from gui.ui_utils import create_table

class ProjectAmpliconRunsWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle("Runs & Amplicon Types")
        self.resize(800, 500)

        main_layout = QVBoxLayout()
        tabs = QTabWidget()

        # Sequencing Runs Tab
        seq = QWidget()
        seq_layout = QVBoxLayout()

        try:
            runs = get_project_sequencing_runs(self.project_id)
            seq_layout.addWidget(QLabel(f"Sequencing Runs ({len(runs)} rows)"))
            seq_layout.addWidget(create_table(runs))
        except Exception as e:
            seq_layout.addWidget(QLabel(f"Error: {e}"))

        seq.setLayout(seq_layout)

        # Amplicon Types Tab
        amp = QWidget()
        amp_layout = QVBoxLayout()

        try:
            amp_types = get_project_amplicon_types(self.project_id)
            amp_layout.addWidget(QLabel(f"Amplicon Types ({len(amp_types)} rows)"))
            amp_layout.addWidget(create_table(amp_types))
        except Exception as e:
            amp_layout.addWidget(QLabel(f"Error: {e}"))

        amp.setLayout(amp_layout)

        # Add tabs
        tabs.addTab(seq, "Sequencing Runs")
        tabs.addTab(amp, "Amplicon Types")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
