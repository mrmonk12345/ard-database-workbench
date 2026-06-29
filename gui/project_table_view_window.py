import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog
)

from gui.ui_utils import create_table


class ProjectTableViewWindow(QDialog):
    def __init__(
        self,
        parent=None,
        project_id=None,
        table_name="Table",
        get_data_func=None,
        output_filename="table.tsv"
    ):
        super().__init__(parent)

        self.project_id = project_id
        self.table_name = table_name
        self.get_data_func = get_data_func
        self.output_filename = output_filename

        self.setWindowTitle(self.table_name)
        self.resize(500, 400)

        layout = QVBoxLayout()

        try:
            # ✅ fetch data (expected DataFrame)
            df = self.get_data_func(self.project_id)

            self.data = df.to_dict("records")
            self.columns = list(df.columns)

            layout.addWidget(QLabel(f"{self.table_name} ({len(self.data)} rows)"))

            # ✅ table view
            table = create_table(df)
            layout.addWidget(table)

            # ✅ download button
            btn = QPushButton("Download TSV")
            btn.clicked.connect(self.download_tsv)
            layout.addWidget(btn)

        except Exception as e:
            layout.addWidget(QLabel(f"Error fetching data: {e}"))

        self.setLayout(layout)

    # ======================
    # TSV EXPORT
    # ======================
    def download_tsv(self):
        if not hasattr(self, "data") or not self.data:
            print("No data to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save TSV",
            self.output_filename,
            "TSV Files (*.tsv)"
        )

        if not file_path:
            return

        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns, delimiter="\t")
            writer.writeheader()
            writer.writerows(self.data)

        print(f"TSV saved to {file_path}")
