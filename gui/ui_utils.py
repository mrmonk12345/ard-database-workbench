from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QColor, QFont

def create_table(df, highlight_ids=None, id_column="id"):
    table = QTableWidget()

    if df is None or df.empty:
        return QLabel("No data")

    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns.tolist())

    for i in range(len(df)):
        for j in range(len(df.columns)):
            value = str(df.iat[i, j])
            item = QTableWidgetItem(value)

            # ✅ Highlight logic
            if highlight_ids is not None and id_column in df.columns:
                row_id = df.iloc[i][id_column]
                if row_id in highlight_ids:
                    item.setBackground(QColor(200, 255, 200))  # light green
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

            table.setItem(i, j, item)

    table.resizeColumnsToContents()
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)

    return table

def create_fillable_table(columns, rows=5):
    table = QTableWidget(rows, len(columns))
    table.setHorizontalHeaderLabels(columns)

    # Fill cells with empty items so user can click immediately
    for row in range(rows):
        for col in range(len(columns)):
            table.setItem(row, col, QTableWidgetItem(""))

    return table

def table_to_dicts(table):
    """Convert QTableWidget to list of dicts (skip empty rows)."""
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

        # ✅ skip completely empty rows
        if not is_empty:
            data.append(row_data)

    return data
