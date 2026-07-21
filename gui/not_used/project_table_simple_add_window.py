import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QHBoxLayout, QSpinBox
)

from scripts.python.db_get_columns import get_table_columns

from gui.tsv_exporter import TSVExporter


class ProjectTableSimpleAddWindow(QDialog):
    def __init__(
        self,
        parent=None,
        project_id=None,
        table_name=None,
        pk_column=None,
        output_filename="table.tsv"
    ):
        super().__init__(parent)

        self.project_id = project_id
        self.table_name = table_name
        self.pk_column = pk_column
        self.output_filename = output_filename

        self.setWindowTitle(f"Add to {self.table_name}")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # ✅ Instructions
        layout.addWidget(QLabel(
            "Download TSV → fill manually → run:\n"
            "input_table.sh --input table.tsv"
        ))

        # ✅ Row count selector
        row_layout = QHBoxLayout()
        self.row_count = QSpinBox()
        self.row_count.setMinimum(1)
        self.row_count.setMaximum(10000)
        self.row_count.setValue(5)

        row_layout.addWidget(QLabel("Rows:"))
        row_layout.addWidget(self.row_count)
        layout.addLayout(row_layout)

        # ✅ Button
        btn = QPushButton("Download TSV Template")
        btn.clicked.connect(self.download_tsv)
        layout.addWidget(btn)

    def download_tsv(self):
        columns = get_table_columns(self.table_name)

        # ✅ remove PK only
        columns = [c for c in columns if c != self.pk_column]

        # ✅ prepare data
        data = []
        for _ in range(self.row_count.value()):
            row = {col: "" for col in columns}

            if "project_id" in columns:   # ✅ fix (not "in row")
                row["project_id"] = self.project_id

            data.append(row)

        # ✅ use exporter
        exporter = TSVExporter(self)
        file_path = exporter.save(data, columns, self.output_filename)

        # ✅ close dialog ONLY if save succeeded
        if file_path:
            self.accept()