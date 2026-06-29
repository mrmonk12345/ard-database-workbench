import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QWidget, QSplitter, QFileDialog
)
from PyQt6.QtCore import Qt

from gui.ui_utils import create_matrix_table, extract_matrix_selection

from scripts.python.project_get_data import get_project_samples
from scripts.python.project_get_data import get_project_amplicon_types
from scripts.python.db_get_columns import get_table_columns


class ProjectLibrariesAddWindowNew(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle("Add Libraries")
        self.resize(1000, 650)

        main_layout = QVBoxLayout()

        # ======================
        # LOAD DATA
        # ======================
        self.samples_df = get_project_samples(project_id)
        self.samples = self.samples_df.to_dict("records")

        self.amplicons_df = get_project_amplicon_types(self.project_id)
        self.amplicons = self.amplicons_df.to_dict("records")

        # ======================
        # BOTTOM (MATRIX + BUTTON)
        # ======================
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()

        # ✅ Instructions
        bottom_layout.addWidget(QLabel(
            "1. Select sample / amplicon combinations\n"
            "2. Click 'Download TSV'\n"
            "3. Run:\n"
            "   input_table.sh --input libraries.tsv"
        ))

        # ✅ Matrix table
        self.table = create_matrix_table(
            rows_data=self.samples,
            cols_data=self.amplicons,
            row_id_key="sample_id",
            row_label_key="sample_label",
            col_id_key="amplicon_type_id"
        )

        bottom_layout.addWidget(self.table)

        # ✅ Download button
        btn = QPushButton("Download TSV")
        btn.clicked.connect(self.download_tsv)
        bottom_layout.addWidget(btn)

        bottom_widget.setLayout(bottom_layout)

        # ======================
        # SPLITTER
        # ======================
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(bottom_widget)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    # ======================
    # TSV EXPORT
    # ======================
    def download_tsv(self):
        data = extract_matrix_selection(
            table=self.table,
            rows_data=self.samples,
            cols_data=self.amplicons,
            row_id_key="sample_id",
            col_id_key="amplicon_type_id"
        )

        if not data:
            print("No selections")
            return

        # ✅ Get DB columns for libraries table
        columns = get_table_columns("libraries")

        # ✅ Remove PK (assumed)
        pk = "library_id"
        columns = [c for c in columns if c != pk]

        # ✅ Keep only relevant columns that exist in matrix + project_id
        allowed = {"project_id", "sample_id", "amplicon_type_id"}
        columns = [c for c in columns if c in allowed]

        # Ensure correct order
        columns = ["project_id", "sample_id", "amplicon_type_id"]

        # ✅ Ask save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save TSV",
            "libraries.tsv",
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return

        # ✅ Write TSV
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
            writer.writeheader()

            for row in data:
                writer.writerow({
                    "project_id": self.project_id,
                    "sample_id": row["sample_id"],
                    "amplicon_type_id": row["amplicon_type_id"]
                })

        print(f"TSV saved to {file_path}")

        self.accept()