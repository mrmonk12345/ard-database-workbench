"""Provide a reusable dialog for exporting records as TSV files."""

import csv
from PyQt6.QtWidgets import QFileDialog


class TSVExporter:
    """Save tabular records to a user-selected TSV file."""
    def __init__(self, parent=None):
        """Initialize the exporter.

        Args:
            parent: Optional Qt widget that owns the save dialog.
        """
        self.parent = parent

    def save(self, data, columns, default_filename="output.tsv", default_output_directory="input_staging",):
        """Write records to a TSV file selected by the user.

        Args:
            data: Iterable of dictionaries containing the records to export.
            columns: Column names used for the TSV header and row order.
            default_filename: Suggested filename in the save dialog.
            default_output_directory: Suggested starting directory.

        Returns:
            The saved file path, or ``None`` if there is no data or the user
            cancels the save dialog.
        """
        # Do not open a save dialog when there are no records to export.
        if not data:
            print("No data to export")
            return None

        # Ask the user where to save the TSV file.
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save TSV",
            f"{default_output_directory}/{default_filename}",
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return None

        # Write the header and records using tab-separated formatting.
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
            writer.writeheader()
            writer.writerows(data)

        print(f"TSV saved to {file_path}")
        return file_path
