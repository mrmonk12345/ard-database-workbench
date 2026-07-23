"""Provide a matrix-based interface for generating relationship-table TSV files."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QWidget, QSplitter, QFileDialog, QTableWidgetItem
)
from PyQt6.QtCore import Qt

from gui.ui_utils import create_matrix_table, extract_matrix_selection

from scripts.python.db_get_columns import get_table_columns

from gui.tsv_exporter import TSVExporter

class TableMatrixAddWindow(QDialog):
    """
    Generate a TSV file from selected row-and-column combinations.

    The matrix represents relationships between two entity types, such as
    libraries and sequencing runs or samples and amplicon types.
    """

    def __init__(
        self,
        parent=None,
        entity_id=None,
        entity_column=None,
        table_name=None,
        pk_column=None,
        rows_data=None,
        cols_data=None,
        row_id_key="id",
        row_label_key="label",
        col_id_key="id",
        output_filename="output.tsv"
    ):
        """
        Initialize the matrix selection window.

        Args:
            parent: Optional parent Qt widget.
            entity_id: ID of the parent entity to include in exported rows.
            entity_column: Database column for the parent entity ID.
            table_name: Database table used to determine TSV columns.
            pk_column: Auto-generated primary key column to exclude.
            rows_data: Records displayed as matrix rows.
            cols_data: Records displayed as matrix columns.
            row_id_key: ID field used for row records.
            row_label_key: Display label field used for row records.
            col_id_key: ID field used for column records.
            output_filename: Default name for the exported TSV file.
        """
        super().__init__(parent)

        # Store the configuration used to build and export the matrix.
        self.entity_id = entity_id
        self.entity_column = entity_column
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

        # Create the main layout and the matrix container.
        main_layout = QVBoxLayout()
        container = QWidget()
        layout = QVBoxLayout()

        # Explain how to select combinations and export the TSV file.
        layout.addWidget(QLabel(
            "1. Select combinations in the matrix\n"
            "2. Click 'Download TSV'\n"
            "3. Run:\n"
            "   input_table.sh --input file.tsv"
        ))

        # Show the entity types represented by the matrix axes.
        title = QLabel(f"<b>{self.row_id_key} x {self.col_id_key}</b>")
        layout.addWidget(title)

        # Build the selectable matrix from the supplied row and column data.
        self.table = create_matrix_table(
            rows_data=self.rows_data,
            cols_data=self.cols_data,
            row_id_key=self.row_id_key,
            row_label_key=self.row_label_key,
            col_id_key=self.col_id_key
        )

        # Allow users to select or clear an entire matrix column.        
        self.table.horizontalHeader().sectionClicked.connect(self.toggle_column)
        
        layout.addWidget(self.table)

        # Export the selected combinations when clicked.
        btn = QPushButton("Download TSV")
        btn.clicked.connect(self.download_tsv)
        layout.addWidget(btn)

        container.setLayout(layout)

        # Use a splitter so the layout can be extended later if needed.
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(container)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        
    def toggle_column(self, col_index):
        """
        Toggle all selectable cells in a matrix column.

        If at least one cell is unchecked, all cells in the column are checked.
        Otherwise, all cells in the column are unchecked. The first two columns
        contain row information and are not selectable.
        """
      
        if col_index < 2:
            return  # skip first 2 columns

    
        table = self.table
        row_count = table.rowCount()
    
        # Check whether the column contains an unchecked cell.
        should_check = False
        for row in range(row_count):
            item = table.item(row, col_index)
            if item and item.checkState() != Qt.CheckState.Checked:
                should_check = True
                break
    

        new_state = Qt.CheckState.Checked if should_check else Qt.CheckState.Unchecked

        # Apply the selected state to every cell in the column.
        for row in range(row_count):
            item = table.item(row, col_index)
            if item:
                item.setCheckState(new_state)
              

    def download_tsv(self):
        """Export selected matrix combinations as a database-ready TSV file."""
        # Convert checked matrix cells into relationship records.
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

        # Get the destination table columns and exclude its generated ID.
        columns = get_table_columns(self.table_name)
        columns = [c for c in columns if c != self.pk_column]

        # Add required values while leaving other table columns blank.
        cleaned_data = []
        for row in data:
            row_dict = {col: "" for col in columns}

            if (
                self.entity_column
                and self.entity_column in columns
            ):
                row[self.entity_column] = self.entity_id

            if self.row_id_key in columns:
                row_dict[self.row_id_key] = row[self.row_id_key]

            if self.col_id_key in columns:
                row_dict[self.col_id_key] = row[self.col_id_key]

            cleaned_data.append(row_dict)

        # Open the save dialog and write the selected records to TSV.
        exporter = TSVExporter(self)
        file_path = exporter.save(cleaned_data, columns, self.output_filename)

        # Close the dialog only when the file was successfully saved.
        if file_path:
            self.accept()