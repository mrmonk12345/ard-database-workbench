import csv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QWidget, QSplitter, QFileDialog, QTableWidgetItem
)
from PyQt6.QtCore import Qt

from gui.ui_utils import create_matrix_table, extract_matrix_selection

from scripts.python.db_get_columns import get_table_columns

from gui.tsv_expoorter import TSVExporter

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
        
        self.table.horizontalHeader().sectionClicked.connect(self.toggle_column)
        
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

        
    def toggle_column(self, col_index):
      """
      Toggle all checkboxes in a column.
      If at least one is unchecked → check all
      Otherwise → uncheck all
      """
      
      if col_index < 2:
          return  # skip first 2 columns

  
      table = self.table
      row_count = table.rowCount()
  
      # Detect if we should check or uncheck
      should_check = False
      for row in range(row_count):
          item = table.item(row, col_index)
          if item and item.checkState() != Qt.CheckState.Checked:
              should_check = True
              break
  
      # Apply state
      new_state = Qt.CheckState.Checked if should_check else Qt.CheckState.Unchecked
  
      for row in range(row_count):
          item = table.item(row, col_index)
          if item:
              item.setCheckState(new_state)
              
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

        # ✅ columns, remove PK only
        columns = get_table_columns(self.table_name)
        columns = [c for c in columns if c != self.pk_column]

        # ✅ prepare cleaned data
        cleaned_data = []
        for row in data:
            row_dict = {col: "" for col in columns}

            if "project_id" in columns:
                row_dict["project_id"] = self.project_id

            if self.row_id_key in columns:
                row_dict[self.row_id_key] = row[self.row_id_key]

            if self.col_id_key in columns:
                row_dict[self.col_id_key] = row[self.col_id_key]

            cleaned_data.append(row_dict)

        # ✅ use exporter
        exporter = TSVExporter(self)
        file_path = exporter.save(cleaned_data, columns, self.output_filename)

        # ✅ only close dialog if saved
        if file_path:
            self.accept()