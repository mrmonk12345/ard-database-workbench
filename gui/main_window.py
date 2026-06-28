from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTabWidget, QLabel, QComboBox
)

from gui.project_data_window import ProjectDataWindow
from scripts.python.db_get_data import get_project_ids
            
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARD Database GUI")

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.project_tab(), "Project")
        self.tabs.addTab(self.dataset_tab(), "Datasets")
        self.tabs.addTab(self.dataset_tab(), "Setup")

        layout.addWidget(self.tabs)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def project_tab(self):
        from PyQt6.QtWidgets import QWidget, QVBoxLayout

        widget = QWidget()
        layout = QVBoxLayout()

        self.project_selector = QComboBox()

        # Get DataFrame
        df = get_project_ids()

        if not df.empty:
            # Add items with ID stored as userData
            for _, row in df.iterrows():
                self.project_selector.addItem(str(row["project_id"]), int(row["project_id"]))



        layout.addWidget(QLabel("Select Project:"))
        layout.addWidget(self.project_selector)


        enter_btn = QPushButton("Open Project")
        enter_btn.clicked.connect(lambda: self.open_project_dashboard(self.project_selector.currentData()))

        layout.addWidget(enter_btn)

        widget.setLayout(layout)
        return widget

    def dataset_tab(self):
        from PyQt6.QtWidgets import QWidget, QVBoxLayout

        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QPushButton("Export Manifest"))

        widget.setLayout(layout)
        return widget

    def open_project_dashboard(self, project_id=None):
        if project_id is None:
            project_id = self.project_selector.currentData()

        self.log.append(f"Opened Project {project_id}")

        self.project_window = ProjectDataWindow(self, project_id=project_id)
        self.project_window.exec()