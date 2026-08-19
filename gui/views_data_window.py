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
from gui.views_sections import (
    ncbi_view_section,
    pipeline_runs_view_section,
)


class ViewsDataWindow(QDialog):
    """Dialog for browsing database views."""

    def __init__(self, parent=None):
        """Initialize the general tables dialog."""
        super().__init__(parent)

        self.setWindowTitle("Database Views")
        self.resize(600, 900)

        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        layout = QVBoxLayout(content)

        layout.addWidget(QLabel("Browse views:"))
    
        sections = [
            ncbi_view_section(self),
            pipeline_runs_view_section(self),
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
        """Open a table view window for a specific SQL view."""
        self.window = TableViewWindow(
            self,
            dataframe=dataframe,
            table_name=table_name,
            output_filename=filename,
        )
        self.window.show()
