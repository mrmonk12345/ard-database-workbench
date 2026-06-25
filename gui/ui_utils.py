from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel

def create_table(df):
    table = QTableWidget()

    if df is None or df.empty:
        return QLabel("No data")

    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns.tolist())

    for i in range(len(df)):
        for j in range(len(df.columns)):
            table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

    table.resizeColumnsToContents()
    table.setAlternatingRowColors(True)
    table.setSortingEnabled(True)

    return table