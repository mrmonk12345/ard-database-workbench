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

    def __init__(
        self,
        parent=None,
        entity_id=None,
        entity_column=None,
        table_name=None,
        pk_column=None,
        output_filename="table.tsv",
    ):
        super().__init__(parent)

        self.entity_id = entity_id
        self.entity_column = entity_column
        self.table_name = table_name
        self.pk_column = pk_column
        self.output_filename = output_filename

        self.setWindowTitle(
            f"Add to {self.table_name}"
        )

        self.resize(400, 200)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(
                "Download TSV ? fill manually ? run:\n"
                "input_table.sh --input table.tsv"
            )
        )

        row_layout = QHBoxLayout()

        self.row_count = QSpinBox()

        self.row_count.setMinimum(1)
        self.row_count.setMaximum(10000)
        self.row_count.setValue(5)

        row_layout.addWidget(
            QLabel("Rows:")
        )

        row_layout.addWidget(
            self.row_count
        )

        layout.addLayout(row_layout)

        btn = QPushButton(
            "Download TSV Template"
        )

        btn.clicked.connect(
            self.download_tsv
        )

        layout.addWidget(btn)

    def download_tsv(self):

        columns = get_table_columns(
            self.table_name
        )

        columns = [
            c
            for c in columns
            if c != self.pk_column
        ]

        data = []

        for _ in range(
            self.row_count.value()
        ):

            row = {
                col: ""
                for col in columns
            }

            # Generic parent ID support
            if (
                self.entity_column
                and self.entity_column in columns
            ):
                row[self.entity_column] = self.entity_id
                
            data.append(row)

        exporter = TSVExporter(self)

        file_path = exporter.save(
            data,
            columns,
            self.output_filename,
        )

        if file_path:
            self.accept()