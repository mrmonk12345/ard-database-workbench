"""Display sequencing runs and amplicon types associated with a project."""

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
    """Show project-related sequencing runs and amplicon types."""

    def __init__(self, parent=None, project_id=None):
        """
        Initialize the window for the selected project.

        Args:
            parent: Optional parent Qt widget.
            project_id: ID of the project whose records should be highlighted.
        """
        super().__init__(parent)
        self.project_id = project_id

        self.setWindowTitle("Runs & Amplicon Types")
        self.resize(800, 500)

        # Create the main layout and tab container.
        main_layout = QVBoxLayout()
        tabs = QTabWidget()

        # Add a tab showing all sequencing runs, with project runs highlighted.
        tabs.addTab(
            self._create_table_tab(
                title="Sequencing Runs",
                get_all_fn=get_sequencing_runs,
                get_project_fn=get_project_sequencing_runs,
                id_column="sequencing_run_id"
            ),
            "Sequencing Runs"
        )

        # Add a tab showing all amplicon types, with project types highlighted.
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
        """
        Create a table tab and highlight records belonging to the project.

        Args:
            title: Title displayed above the table.
            get_all_fn: Function returning all records of the selected type.
            get_project_fn: Function returning project-specific records.
            id_column: Column used to identify and highlight project records.

        Returns:
            A QWidget containing the table and its descriptive label.
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)

        try:
            # Retrieve all records and the records associated with the project.
            all_data = get_all_fn()
            project_data = get_project_fn(self.project_id)

            # Build a set for quick lookup when highlighting table rows.
            project_ids = set(project_data[id_column].tolist())

            # Display all records and highlight project-specific records.
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
