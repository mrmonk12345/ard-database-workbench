"""Provide a form for generating TSV templates for database records."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSpinBox,
)

from scripts.python.db_get_columns import get_table_columns
from gui.tsv_exporter import TSVExporter


class TableSimpleAddWindow(QDialog):
    """Generate a blank TSV template for adding records to a table."""

    def __init__(
        self,
        parent=None,
        entity_id=None,
        entity_column=None,
        table_name=None,
        pk_column=None,
        output_filename="table.tsv",
    ):
        """
        Initialize the TSV-template dialog.

        Args:
            parent: Optional parent Qt widget.
            entity_id: ID of the parent entity for the new records.
            entity_column: Column that stores the parent entity ID.
            table_name: Destination database table.
            pk_column: Auto-generated primary-key column to exclude.
            output_filename: Default name for the exported TSV file.
        """
        super().__init__(parent)

        # Store the table and parent-entity information for export.
        self.entity_id = entity_id
        self.entity_column = entity_column
        self.table_name = table_name
        self.pk_column = pk_column
        self.output_filename = output_filename

        self.setWindowTitle(
            f"Add to {self.table_name}"
        )
        self.resize(400, 200)

        # Create the dialog's main layout.
        layout = QVBoxLayout(self)

        # Explain how the generated template should be used.
        layout.addWidget(
            QLabel(
                "Download TSV ? fill manually ? run:\n"
                "input_table.sh --input table.tsv"
            )
        )

        # Add a control for selecting the number of template rows.
        row_layout = QHBoxLayout()

        self.row_count = QSpinBox()
        self.row_count.setMinimum(1)
        self.row_count.setMaximum(10000)
        self.row_count.setValue(5)

        row_layout.addWidget(QLabel("Rows:"))
        row_layout.addWidget(self.row_count)
        layout.addLayout(row_layout)

        # Create the template when the button is clicked.
        btn = QPushButton("Download TSV Template")
        btn.clicked.connect(self.download_tsv)
        layout.addWidget(btn)

    def download_tsv(self):
        """Create and save a blank TSV template for the selected table."""
        # Read the table schema to determine the TSV columns.
        columns = get_table_columns(
            self.table_name
        )

        # Generated primary keys should not be supplied by the user.
        columns = [
            c
            for c in columns
            if c != self.pk_column
        ]

        data = []

        # Create the requested number of blank rows.
        for _ in range(
            self.row_count.value()
        ):

            row = {
                col: ""
                for col in columns
            }

            # Pre-fill the parent entity column when applicable.
            if (
                self.entity_column
                and self.entity_column in columns
            ):
                row[self.entity_column] = self.entity_id
                
            data.append(row)

        # Open the save dialog and export the template.
        exporter = TSVExporter(self)
        file_path = exporter.save(
            data,
            columns,
            self.output_filename,
        )
        
        # Close the dialog only after a successful export.
        if file_path:
            self.accept()