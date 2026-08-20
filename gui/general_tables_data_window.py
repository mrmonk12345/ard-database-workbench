"""Display general database tables with selectable view options."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QWidget,
)

from gui.action_box import ActionBox
from gui.table_view_window import TableViewWindow
from gui.general_sections import (
    treatments_section,
    amplicon_types_section,
    projects_section,
    project_amplicon_types_section,
    sequencing_runs_section,
    analysis_datasets_section,
    locations_section,
    rootstocks_section,
    sampling_compartments_section,
    pipeline_runs_section,
)


class GeneralTablesDataWindow(QDialog):
    """Starter window for browsing general tables in the same style as the project/treatment dashboards."""

    def __init__(self, parent=None):
        """Initialize the general tables dialog."""
        super().__init__(parent)

        self.setWindowTitle("General Tables")
        self.resize(600, 900)

        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)

        layout.addWidget(QLabel("Browse general database views:"))

        sections = [
            projects_section(self),
            amplicon_types_section(self),
            project_amplicon_types_section(self),
            sequencing_runs_section(self),
            analysis_datasets_section(self),
            treatments_section(self),
            locations_section(self),
            rootstocks_section(self),
            sampling_compartments_section(self),
            pipeline_runs_section(self),
        ]

        for section in sections:
            layout.addWidget(
                ActionBox(
                    title=section["title"],
                    count=section["count"],
                    buttons=section["buttons"],
                )
            )

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def open_table(self, table_name, dataframe, filename):
        """Open a table view window for a general data set."""
        self.window = TableViewWindow(
            self,
            dataframe=dataframe,
            table_name=table_name,
            output_filename=filename,
        )
        self.window.show()
