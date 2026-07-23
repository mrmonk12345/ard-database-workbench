"""Provide a table widget that supports copying selected cells."""

from PyQt6.QtWidgets import QTableWidget, QApplication
from PyQt6.QtGui import QKeySequence


class CopyableTableWidget(QTableWidget):
    """QTableWidget with tab-separated copy support."""

    def keyPressEvent(self, event):
        """Copy selected cells when the standard Copy shortcut is pressed."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
            return

        # Preserve the default behavior for other key presses.
        super().keyPressEvent(event)

    def copy_selection(self):
        """Copy selected cells to the system clipboard."""
        indexes = self.selectedIndexes()

        if not indexes:
            return

        # Sort cells by row and then by column.
        indexes = sorted(indexes, key=lambda x: (x.row(), x.column()))

        # Group selected cell values by row and column.
        rows = {}
        for idx in indexes:
            rows.setdefault(idx.row(), {})[idx.column()] = idx.data()

        # Format the selected cells as tab-separated rows.
        text = []
        for row in sorted(rows):
            cols = rows[row]
            text.append(
                "\t".join(str(cols.get(col, "")) for col in sorted(cols))
            )

        # Place the formatted text on the system clipboard.
        QApplication.clipboard().setText("\n".join(text))