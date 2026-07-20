from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from gui.ui_utils import create_copyable_table
from gui.tsv_expoorter import TSVExporter


class TableViewWindow(QDialog):
    def __init__(
        self,
        parent=None,
        entity_id=None,
        table_name="Table",
        get_data_func=None,
        output_filename="table.tsv",
    ):
        super().__init__(parent)

        self.entity_id = entity_id
        self.table_name = table_name
        self.get_data_func = get_data_func
        self.output_filename = output_filename

        self.setWindowTitle(table_name)
        self.resize(800, 600)

        layout = QVBoxLayout()

        try:
            if self.get_data_func is None:
                raise ValueError("get_data_func was not provided")

            # Support functions with or without an ID parameter
            if self.entity_id is None:
                df = self.get_data_func()
            else:
                df = self.get_data_func(self.entity_id)

            self.df = df
            self.data = df.to_dict("records")
            self.columns = list(df.columns)

            layout.addWidget(
                QLabel(f"{self.table_name} ({len(self.data)} rows)")
            )

            table = create_copyable_table(df)
            layout.addWidget(table)

            export_btn = QPushButton("Download TSV")
            export_btn.clicked.connect(self.download_tsv)
            layout.addWidget(export_btn)

        except Exception as e:
            layout.addWidget(
                QLabel(f"Error fetching data:\n{str(e)}")
            )

        self.setLayout(layout)

    def download_tsv(self):
        if not hasattr(self, "data"):
            return

        exporter = TSVExporter(self)

        file_path = exporter.save(
            self.data,
            self.columns,
            self.output_filename,
        )

        if file_path:
            self.accept()