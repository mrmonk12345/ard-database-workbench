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