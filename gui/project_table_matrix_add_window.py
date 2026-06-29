import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QWidget, QSplitter, QFileDialog
)
from PyQt6.QtCore import Qt

from gui.ui_utils import create_matrix_table, extract_matrix_selection

from scripts.python.db_get_columns import get_table_columns

class ProjectTableMatrixAddWindow(QDialog):
    """
    Generic matrix-based TSV generator.

    Use this for any:
    row entities × column entities → relationship table
    """

    def __init__(
        self,
        parent=None,
        project_id=None,
        table_name=None,
        pk_column=None,
        rows_data=None,
        cols_data=None,
        row_id_key="id",
        row_label_key="label",
        col_id_key="id",
        output_filename="output.tsv"
    ):
        super().__init__(parent)

        self.project_id = project_id
        self.table_name = table_name
        self.pk_column = pk_column
        self.rows_data = rows_data or []
        self.cols_data = cols_data or []
        self.row_id_key = row_id_key
        self.row_label_key = row_label_key
        self.col_id_key = col_id_key
        self.output_filename = output_filename

        self.setWindowTitle("Matrix Add (TSV Export)")
        self.resize(500, 400)

        main_layout = QVBoxLayout()

        # ======================
        # BOTTOM (UI)
        # ======================
        container = QWidget()
        layout = QVBoxLayout()

        # ✅ Instructions
        layout.addWidget(QLabel(
            "1. Select combinations in the matrix\n"
            "2. Click 'Download TSV'\n"
            "3. Run:\n"
            "   input_table.sh --input file.tsv"
        ))

        # Table title
        title = QLabel(f"<b>{self.row_id_key} × {self.col_id_key}</b>")
        layout.addWidget(title)

        # ✅ Matrix table
        self.table = create_matrix_table(
            rows_data=self.rows_data,
            cols_data=self.cols_data,
            row_id_key=self.row_id_key,
            row_label_key=self.row_label_key,
            col_id_key=self.col_id_key
        )

        layout.addWidget(self.table)

        # ✅ Button
        btn = QPushButton("Download TSV")
        btn.clicked.connect(self.download_tsv)
        layout.addWidget(btn)

        container.setLayout(layout)

        # ✅ Splitter (future extensibility)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(container)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    # ======================
    # TSV EXPORT
    # ======================
    def download_tsv(self):
        data = extract_matrix_selection(
            table=self.table,
            rows_data=self.rows_data,
            cols_data=self.cols_data,
            row_id_key=self.row_id_key,
            col_id_key=self.col_id_key
        )

        if not data:
            print("No selections")
            return

        # columns, remove PK only
        columns = get_table_columns(self.table_name)
        columns = [c for c in columns if c != self.pk_column]

        # ✅ Ask save location
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
            writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
            writer.writeheader()

            for row in data:
                row_dict = {col: "" for col in columns}  # ✅ initialize all columns

                # ✅ fill required fields
                if "project_id" in columns:
                    row_dict["project_id"] = self.project_id

                if self.row_id_key in columns:
                    row_dict[self.row_id_key] = row[self.row_id_key]

                if self.col_id_key in columns:
                    row_dict[self.col_id_key] = row[self.col_id_key]

                writer.writerow(row_dict)

        print(f"TSV saved to {file_path}")

        self.accept()