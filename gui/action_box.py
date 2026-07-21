from PyQt6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from PyQt6.QtCore import Qt


class ActionBox(QGroupBox):

    def __init__(
        self,
        title,
        count,
        buttons,
        parent=None,
    ):
        super().__init__(title, parent)

        layout = QVBoxLayout()

        count_label = QLabel(str(count))
        count_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        count_label.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        layout.addWidget(count_label)

        button_layout = QHBoxLayout()

        for btn_text, callback in buttons:

            btn = QPushButton(btn_text)
            btn.clicked.connect(callback)

            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)