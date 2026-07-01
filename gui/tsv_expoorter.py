import csv
from PyQt6.QtWidgets import QFileDialog


class TSVExporter:
    def __init__(self, parent=None):
        self.parent = parent

    def save(self, data, columns, default_filename="output.tsv", default_output_directory="input_staging",):
        if not data:
            print("No data to export")
            return None

        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save TSV",
            f"{default_output_directory}/{default_filename}",
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return None

        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
            writer.writeheader()
            writer.writerows(data)

        print(f"TSV saved to {file_path}")
        return file_path
