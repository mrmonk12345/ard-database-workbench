"""Reusable Qt helpers for displaying and editing tabular data."""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

from gui.copyable_table_widget import CopyableTableWidget

def create_table(df, highlight_ids=None, id_column="id"):
    """Create a table widget from a pandas DataFrame.

    Args:
        df: DataFrame containing the records to display.
        highlight_ids: Optional collection of IDs whose rows should be
            highlighted.
        id_column: Column used to compare values with ``highlight_ids``.

    Returns:
        A QTableWidget containing the data, or a QLabel when no data exists.
    """
    table = QTableWidget()

    if df is None or df.empty:
        return QLabel("No data")

    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns.tolist())

    # Populate the table cell by cell.
    for i in range(len(df)):
        for j in range(len(df.columns)):
            value = str(df.iat[i, j])
            item = QTableWidgetItem(value)

            # Highlight cells belonging to selected records.
            if highlight_ids is not None and id_column in df.columns:
                row_id = df.iloc[i][id_column]
                if row_id in highlight_ids:
                    item.setBackground(QColor(200, 255, 200))  # light green
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

            table.setItem(i, j, item)

    # Improve table readability and usability.
    table.resizeColumnsToContents()
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)

    return table


def create_copyable_table(df, highlight_ids=None, id_column="id"):
    """Create a copy-enabled table widget from a pandas DataFrame.

    Args:
        df: DataFrame containing the records to display.
        highlight_ids: Optional collection of IDs whose rows should be
            highlighted.
        id_column: Column used to compare values with ``highlight_ids``.

    Returns:
        A CopyableTableWidget containing the data, or a QLabel when no data
        exists.
    """
    table = CopyableTableWidget()

    if df is None or df.empty:
        return QLabel("No data")

    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns.tolist())

    # Populate the table cell by cell.
    for i in range(len(df)):
        for j in range(len(df.columns)):
            value = str(df.iat[i, j])
            item = QTableWidgetItem(value)

            # Highlight cells belonging to selected records.
            if highlight_ids is not None and id_column in df.columns:
                row_id = df.iloc[i][id_column]
                if row_id in highlight_ids:
                    item.setBackground(QColor(200, 255, 200))  # light green
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

            table.setItem(i, j, item)

    # Configure the table for convenient viewing and sorting.
    table.resizeColumnsToContents()
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)

    return table
    
    
def create_fillable_table(columns, rows=5):
    """Create an editable table initialized with blank cells.

    Args:
        columns: Column names to display.
        rows: Number of blank rows to create.

    Returns:
        A QTableWidget with editable, empty cells.
    """
    table = QTableWidget(rows, len(columns))
    table.setHorizontalHeaderLabels(columns)

    # Fill cells with empty items so user can click immediately
    for row in range(rows):
        for col in range(len(columns)):
            table.setItem(row, col, QTableWidgetItem(""))

    return table

def table_to_dicts(table):
    """Convert a QTableWidget into a list of dictionaries.

    Completely empty rows are omitted. Empty cells in non-empty rows are
    represented by ``None``.

    Args:
        table: QTableWidget containing the records to convert.

    Returns:
        A list of dictionaries keyed by the table's header labels.
    """
    data = []

    for row in range(table.rowCount()):
        row_data = {}
        is_empty = True

        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            header = header_item.text() if header_item else f"col_{col}"

            item = table.item(row, col)
            value = item.text().strip() if item and item.text() else None

            if value:
                is_empty = False

            row_data[header] = value

        # Exclude rows in which every cell is empty.
        if not is_empty:
            data.append(row_data)

    return data


def create_matrix_table(
    rows_data,
    cols_data,
    row_id_key,
    row_label_key,
    col_id_key
):
    """Create a checkable matrix for selecting relationships.

    The first two columns contain the row ID and label. Each remaining column
    represents an ID from ``cols_data`` and contains a checkable cell.

    Args:
        rows_data: Records represented by matrix rows.
        cols_data: Records represented by matrix columns.
        row_id_key: ID key for row records.
        row_label_key: Display-label key for row records.
        col_id_key: ID key for column records.

    Returns:
        A QTableWidget containing the relationship matrix.
    """
    table = QTableWidget(len(rows_data), len(cols_data) + 2)

    # Build dynamic headers from the supplied row and column data.
    headers = [row_id_key, row_label_key] + [
        str(col[col_id_key]) for col in cols_data
    ]
    table.setHorizontalHeaderLabels(headers)

    # Populate each matrix row.
    for row_idx, row in enumerate(rows_data):
        # Add the row ID as a read-only cell.
        id_item = QTableWidgetItem(str(row.get(row_id_key, "")))
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_idx, 0, id_item)

        # Add the row label as a read-only cell.
        label_item = QTableWidgetItem(str(row.get(row_label_key, "")))
        label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row_idx, 1, label_item)

        # Add one unchecked checkbox cell for each column record.
        for col_idx, col in enumerate(cols_data, start=2):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            checkbox.setCheckState(Qt.CheckState.Unchecked)

            table.setItem(row_idx, col_idx, checkbox)

    table.resizeColumnsToContents()

    return table

def extract_matrix_selection(
    table,
    rows_data,
    cols_data,
    row_id_key,
    col_id_key
):
    """Extract checked row-and-column combinations from a matrix.

    Args:
        table: Matrix table created by ``create_matrix_table``.
        rows_data: Records represented by matrix rows.
        cols_data: Records represented by matrix columns.
        row_id_key: ID key for row records.
        col_id_key: ID key for column records.

    Returns:
        A list of dictionaries containing selected row/column relationships.
    """
    result = []

    # Matrix data columns begin after the row ID and label columns.
    for row_idx, row in enumerate(rows_data):
        for col_idx, col in enumerate(cols_data, start=2):  # ⚠️ start=2 (important)
            item = table.item(row_idx, col_idx)

            # Add a relationship only when its checkbox is selected.
            if item and item.checkState() == Qt.CheckState.Checked:
                result.append({
                    row_id_key: row[row_id_key],
                    col_id_key: col[col_id_key]
                })

    return result