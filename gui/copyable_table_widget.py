from PyQt6.QtWidgets import QTableWidget, QApplication
from PyQt6.QtGui import QKeySequence


class CopyableTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
            return

        super().keyPressEvent(event)

    def copy_selection(self):
        indexes = self.selectedIndexes()

        if not indexes:
            return

        indexes = sorted(indexes, key=lambda x: (x.row(), x.column()))

        rows = {}
        for idx in indexes:
            rows.setdefault(idx.row(), {})[idx.column()] = idx.data()

        text = []
        for row in sorted(rows):
            cols = rows[row]
            text.append(
                "\t".join(str(cols.get(col, "")) for col in sorted(cols))
            )

        QApplication.clipboard().setText("\n".join(text))