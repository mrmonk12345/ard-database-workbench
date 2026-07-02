from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox
)

from gui.tsv_expoorter import TSVExporter
from scripts.python.


class BaseDatasetTSVWindow(QDialog):
    def __init__(self, parent=None, output_filename="base_dataset.tsv"):
        super().__init__(parent)

        self.output_filename = output_filename

        self.setWindowTitle("Create Base Dataset TSV")
        self.resize(400, 180)

        layout = QVBoxLayout(self)

        # Instructions
        layout.addWidget(QLabel(
            "Select a dataset ID, create the TSV file,\n"
            "fill it manually, then run:\n"
            "input_table.sh --input base_dataset.tsv"
        ))

        # Dataset selector
        dataset_layout = QHBoxLayout()
        self.dataset_id_input = QSpinBox()
        self.dataset_id_input.setMinimum(1)
        self.dataset_id_input.setMaximum(1_000_000)

        dataset_layout.addWidget(QLabel("Dataset ID:"))
        dataset_layout.addWidget(self.dataset_id_input)
        layout.addLayout(dataset_layout)

        # Create button
        btn = QPushButton("Create base_dataset TSV")
        btn.clicked.connect(self.create_tsv)
        layout.addWidget(btn)

    def create_tsv(self):
        dataset_id = self.dataset_id_input.value()

        columns = ["dataset_id", "au_id"]

        data = [{
            "dataset_id": dataset_id,
            "au_id": ""
        }]

        exporter = TSVExporter(self)
        file_path = exporter.save(data, columns, self.output_filename)

        if file_path:
            self.accept()