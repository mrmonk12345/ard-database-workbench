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

        # Tabs
        tabs.addTab(
            self._create_table_tab(
                title="Sequencing Runs",
                get_all_fn=get_sequencing_runs,
                get_project_fn=get_project_sequencing_runs,
                id_column="sequencing_run_id"
            ),
            "Sequencing Runs"
        )

        tabs.addTab(
            self._create_table_tab(
                title="Amplicon Types",
                get_all_fn=get_amplicon_types,
                get_project_fn=get_project_amplicon_types,
                id_column="amplicon_type_id"
            ),
            "Amplicon Types"
        )

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    # =====================
    # Tab builder
    # =====================

    def _create_table_tab(self, title, get_all_fn, get_project_fn, id_column):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        try:
            all_data = get_all_fn()
            project_data = get_project_fn(self.project_id)

            project_ids = set(project_data[id_column].tolist())

            layout.addWidget(QLabel(f"{title} ({len(project_data)} rows). rows are highlighted."))
            layout.addWidget(
                create_table(
                    all_data,
                    highlight_ids=project_ids,
                    id_column=id_column
                )
            )

        except Exception as e:
            layout.addWidget(QLabel(f"Error: {e}"))

        return tab
