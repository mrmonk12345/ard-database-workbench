from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget
)

from scripts.python.project_get_data import (
    get_project_sequencing_runs,
    get_project_amplicon_types
)

from scripts.python.db_get_data import (
    get_amplicon_types,
    get_sequencing_runs
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

        # ================================
        # Sequencing Runs Tab
        # ================================
        seq = QWidget()
        seq_layout = QVBoxLayout()

        try:
            all_runs = get_sequencing_runs()
            project_runs = get_project_sequencing_runs(self.project_id)

            # extract IDs
            project_ids = set(project_runs["sequencing_run_id"].tolist())

            seq_layout.addWidget(QLabel(f"Sequencing Runs ({len(all_runs)} rows)"))
            seq_layout.addWidget(
                create_table(all_runs, highlight_ids=project_ids, id_column="sequencing_run_id")
            )

        except Exception as e:
            seq_layout.addWidget(QLabel(f"Error: {e}"))

        seq.setLayout(seq_layout)

        # ================================
        # Amplicon Types Tab
        # ================================
        amp = QWidget()
        amp_layout = QVBoxLayout()

        try:
            all_amp = get_amplicon_types()
            project_amp = get_project_amplicon_types(self.project_id)

            project_ids = set(project_amp["amplicon_type_id"].tolist())

            amp_layout.addWidget(QLabel(f"Amplicon Types ({len(all_amp)} rows)"))
            amp_layout.addWidget(
                create_table(all_amp, highlight_ids=project_ids, id_column="amplicon_type_id")
            )

        except Exception as e:
            amp_layout.addWidget(QLabel(f"Error: {e}"))

        amp.setLayout(amp_layout)

        # Tabs
        tabs.addTab(seq, "Sequencing Runs")
        tabs.addTab(amp, "Amplicon Types")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)