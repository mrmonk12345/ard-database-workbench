import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QHBoxLayout
)

from scripts.python.db_get_columns import get_table_columns


class ProjectSamplesAddWindowNew(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle(f"Add Samples - Project {self.project_id}")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # ✅ Instruction text
        instruction_label = QLabel(
            "1. Choose number of samples\n"
            "2. Download the TSV template\n"
            "3. Fill in the table\n"
            "4. Run:\n"
            "   input_table.sh --input table.tsv"
        )
        layout.addWidget(instruction_label)

        # ✅ Number of samples selector
        count_layout = QHBoxLayout()
        count_label = QLabel("Number of samples:")
        self.sample_count = QSpinBox()
        self.sample_count.setMinimum(1)
        self.sample_count.setMaximum(10000)
        self.sample_count.setValue(5)

        count_layout.addWidget(count_label)
        count_layout.addWidget(self.sample_count)
        layout.addLayout(count_layout)

        # ✅ Download button
        download_btn = QPushButton("Download TSV Template")
        download_btn.clicked.connect(self.download_tsv_template)
        layout.addWidget(download_btn)

    def download_tsv_template(self):
        # ✅ Get columns
        columns = get_table_columns("samples")

        # ✅ Remove only PK (KEEP project_id now)
        pk = "sample_id"
        columns = [c for c in columns if c != pk]

        # ✅ Ask save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save TSV Template",
            "table.tsv",
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return

        # ✅ Number of rows
        num_rows = self.sample_count.value()

        # ✅ Write TSV
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
            writer.writeheader()

            for _ in range(num_rows):
                row = {col: "" for col in columns}

                # ✅ Fill project_id automatically
                if "project_id" in row:
                    row["project_id"] = self.project_id

                writer.writerow(row)

        print(f"TSV template saved to {file_path}")