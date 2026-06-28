from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget
)

from gui.ui_utils import create_table, create_fillable_table, table_to_dicts

from scripts.python.project_get_data import get_project_samples
from scripts.python.db_get_columns import get_table_columns
from scripts.python.db_insert_rows import insert_rows


class ProjectSamplesAddWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle(f"Add Samples - Project {self.project_id}")
        self.resize(800, 600)

        layout = QVBoxLayout()

        # ======================
        # VIEW (top)
        # ======================
        samples = get_project_samples(self.project_id)

        layout.addWidget(QLabel(f"Samples ({len(samples)} rows)"))
        
        table = create_table(samples)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(table)

        # ======================
        # INPUT TABLE (bottom)
        # ======================
        layout.addWidget(QLabel("Add new samples"))

        columns = get_table_columns("samples")
        
        # Remove primary key and project_id column from input table
        pk = "sample_id"
        project_id_col = "project_id"
        columns = [c for c in columns if c != pk and c != project_id_col]


        self.input_table = create_fillable_table(columns, rows=20)

        layout.addWidget(self.input_table)

        # add row button
        add_row_btn = QPushButton("Add Row")
        add_row_btn.clicked.connect(self.add_row)

        layout.addWidget(add_row_btn)

        # ======================
        # SUBMIT BUTTON
        # ======================
        submit_btn = QPushButton("Insert Samples")
        submit_btn.clicked.connect(self.insert_samples)

        layout.addWidget(submit_btn)

        self.setLayout(layout)

    # ======================
    # LOGIC
    # ======================

    def add_row(self):
        row = self.input_table.rowCount()
        self.input_table.insertRow(row)

        # initialize empty cells (recommended)
        from PyQt6.QtWidgets import QTableWidgetItem

        for col in range(self.input_table.columnCount()):
            self.input_table.setItem(row, col, QTableWidgetItem(""))

    def insert_samples(self):
        rows = table_to_dicts(self.input_table)

        if not rows:
            print("No rows to insert")
            return

        # force project_id
        for row in rows:
            row["project_id"] = self.project_id

        insert_rows("samples", rows)

        print("Inserted samples")

        self.accept()  # ✅ just close window