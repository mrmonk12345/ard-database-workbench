"""Display database records in a table and export them as TSV."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from gui.ui_utils import create_copyable_table
from gui.tsv_exporter import TSVExporter


class TableViewWindow(QDialog):
    """Show a pandas DataFrame in a copyable table."""

    def __init__(
        self,
        parent=None,
        dataframe=None,
        table_name="Table",
        output_filename="table.tsv",
    ):
        """Initialize the table-view dialog.

        Args:
            parent: Optional parent Qt widget.
            dataframe: pandas DataFrame containing the records to display.
            table_name: Title shown in the dialog and row-count label.
            output_filename: Default filename used when exporting TSV data.
        """
        super().__init__(parent)

        self.output_filename = output_filename

        self.setWindowTitle(table_name)
        self.resize(900, 600)

        # Create the dialog's main layout.
        layout = QVBoxLayout()

        try:
            # A DataFrame is required to populate the table.
            if dataframe is None:
                raise ValueError(
                    "Dataframe was not supplied"
                )

            self.df = dataframe

            # Store the records and column names for TSV export.
            self.data = dataframe.to_dict("records")
            self.columns = list(dataframe.columns)

            # Display the table name and number of records.
            layout.addWidget(
                QLabel(
                    f"{table_name} ({len(self.data)} rows)"
                )
            )

            # Create a table that supports copying selected cells.
            table = create_copyable_table(dataframe)
            layout.addWidget(table)

            # Add a button for exporting the displayed records.
            export_btn = QPushButton("Download TSV")
            export_btn.clicked.connect(self.download_tsv)
            layout.addWidget(export_btn)

        except Exception as e:
            layout.addWidget(
                QLabel(f"Error:\n{str(e)}")
            )

        self.setLayout(layout)

    def download_tsv(self):
        """Export the displayed DataFrame records to a TSV file."""
        # Do nothing if the DataFrame was not initialized successfully.
        if not hasattr(self, "data"):
            return

        exporter = TSVExporter(self)

        file_path = exporter.save(
            self.data,
            self.columns,
            self.output_filename,
        )
        
        # Close the dialog only after a successful export.
        if file_path:
            self.accept()