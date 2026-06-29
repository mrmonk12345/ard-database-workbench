import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QFileDialog
)

from gui.ui_utils import create_fillable_table, table_to_dicts
from scripts.python.db_get_columns import get_table_columns


class ProjectTableSimpleAddWindow(QDialog):
    """
    Simple table-based TSV generator.
    User fills rows → exports TSV.
    """

    def __init__(
        self,
        parent=None,
        project_id=None,
        table_name=None,
        pk_column=None,
        output_filename="table.tsv",
        num_rows=5
    ):
        super().__init__(parent)

        self.project_id = project_id
        self.table_name = table_name
        self.pk_column = pk_column
        self.output_filename = output_filename
        self.num_rows = num_rows

        self.setWindowTitle(f"Add to {self.table_name}")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # ======================
        # INSTRUCTIONS
        # ======================
        layout.addWidget(QLabel(
            "1. Fill in the table\n"
            "2. Click 'Download TSV'\n"
            "3. Run:\n"
            "   input_table.sh --input table.tsv"
        ))

        # ======================
        # GET COLUMNS
        # ======================
        columns = get_table_columns(self.table_name)

        # ✅ remove PK only
        exclude = {self.pk_column}
        self.columns = [c for c in columns if c not in exclude]

        # ======================
        # TABLE
        # ======================
        self.table = create_fillable_table(
            columns=self.columns,
            num_rows=self.num_rows
        )

        layout.addWidget(self.table)

        # ======================
        # BUTTON
        # ======================
        btn = QPushButton("Download TSV")
        btn.clicked.connect(self.download_tsv)
        layout.addWidget(btn)

        self.setLayout(layout)

    # ======================
    # EXPORT TSV
    # ======================
    def download_tsv(self):
        data = table_to_dicts(self.table, self.columns)

        if not data:
            print("No data entered")
            return

        # ✅ Ask where to save
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save TSV",
            self.output_filename,
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return

        # ✅ Write TSV
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns, delimiter="\t")
            writer.writeheader()

            for row in data:
                # ✅ auto-fill project_id if exists
                if "project_id" in row:
                    row["project_id"] = self.project_id

                writer.writerow(row)

        print(f"TSV saved to {file_path}")

        self.accept()