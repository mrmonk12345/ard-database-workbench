from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)

from gui.ui_utils import create_copyable_table
from gui.tsv_exporter import TSVExporter


class TableViewWindow(QDialog):

    def __init__(
        self,
        parent=None,
        dataframe=None,
        table_name="Table",
        output_filename="table.tsv",
    ):
        super().__init__(parent)

        self.output_filename = output_filename

        self.setWindowTitle(table_name)
        self.resize(900, 600)

        layout = QVBoxLayout()

        try:

            if dataframe is None:
                raise ValueError(
                    "Dataframe was not supplied"
                )

            self.df = dataframe

            self.data = dataframe.to_dict(
                "records"
            )

            self.columns = list(
                dataframe.columns
            )

            layout.addWidget(
                QLabel(
                    f"{table_name} ({len(self.data)} rows)"
                )
            )

            table = create_copyable_table(
                dataframe
            )

            layout.addWidget(table)

            export_btn = QPushButton(
                "Download TSV"
            )

            export_btn.clicked.connect(
                self.download_tsv
            )

            layout.addWidget(export_btn)

        except Exception as e:

            layout.addWidget(
                QLabel(f"Error:\n{str(e)}")
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