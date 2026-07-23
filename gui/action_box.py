"""Provide a reusable group box with a count and action buttons."""

from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from PyQt6.QtCore import Qt


class ActionBox(QGroupBox):
    """Display a record count and buttons for related actions."""

    def __init__(
        self,
        title,
        count,
        buttons,
        parent=None,
    ):
        """
        Create an action box.

        Args:
            title: Title displayed on the group box.
            count: Numeric value displayed above the buttons.
            buttons: Iterable of ``(text, callback)`` pairs.
            parent: Optional parent Qt widget.
        """
        super().__init__(title, parent)

        # Arrange the count label above the action buttons.
        layout = QVBoxLayout()

        count_label = QLabel(str(count))
        count_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        count_label.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        layout.addWidget(count_label)

        # Create one button for each supplied action.
        button_layout = QHBoxLayout()

        for btn_text, callback in buttons:

            btn = QPushButton(btn_text)
            btn.clicked.connect(callback)

            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        # Apply the completed layout to the group box.
        self.setLayout(layout)