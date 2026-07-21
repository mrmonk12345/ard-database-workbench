from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTabWidget, QLabel, QComboBox
)

import pandas as pd

from gui.project_data_window import ProjectDataWindow
from gui.treatment_data_window import TreatmentDataWindow
from scripts.python.db_get_data import get_projects, get_treatments


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARD Database GUI")

        main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_project_tab(), "Project")
        self.tabs.addTab(self._create_treatment_tab(), "Treatments")
        self.tabs.addTab(self._create_dataset_tab(), "Datasets")
        self.tabs.addTab(self._create_setup_tab(), "Setup")

        main_layout.addWidget(self.tabs)

        # Log area
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

        self.setLayout(main_layout)

    # =====================
    # Tabs
    # =====================

    def _create_project_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.project_selector = QComboBox()
        
        # Load projects
        df = get_projects()
        
        if not df.empty:
            for _, row in df.iterrows():
                label = row["label"]
        
                text = (
                    f"{row['project_id']} - {label}"
                    if pd.notna(label) and str(label).strip()
                    else str(row["project_id"])
                )
        
                self.project_selector.addItem(
                    text,
                    int(row["project_id"])
                )

        layout.addWidget(QLabel("Select Project:"))
        layout.addWidget(self.project_selector)

        enter_btn = QPushButton("Open Project")
        enter_btn.clicked.connect(self._handle_open_project)

        layout.addWidget(enter_btn)

        return widget

    def _create_treatment_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.treatment_selector = QComboBox()
        
        # Load projects
        df = get_treatments()
        
        if not df.empty:
            for _, row in df.iterrows():
                name = row["name"]
        
                text = (
                    f"{row['treatment_id']} - {name}"
                    if pd.notna(name) and str(name).strip()
                    else str(row["treatment_id"])
                )
        
                self.treatment_selector.addItem(
                    text,
                    int(row["treatment_id"])
                )

        layout.addWidget(QLabel("Select Treatment:"))
        layout.addWidget(self.treatment_selector)

        enter_btn = QPushButton("Open Treatment")
        enter_btn.clicked.connect(self._handle_open_treatment)

        layout.addWidget(enter_btn)

        return widget

    def _create_dataset_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        export_btn = QPushButton("Export Manifest")
        export_btn.clicked.connect(self._handle_export_manifest)

        layout.addWidget(export_btn)

        return widget

    def _create_setup_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("Setup options will go here"))

        return widget

    # =====================
    # Handlers / Actions
    # =====================

    def _handle_open_project(self):
        project_id = self.project_selector.currentData()
        self.open_project_dashboard(project_id)
    
    def _handle_open_treatment(self):
        treatment_id = self.treatment_selector.currentData()
        self.open_treatment_dashboard(treatment_id)

    def _handle_export_manifest(self):
        self.log.append("Export Manifest clicked")

    # =====================
    # Logic
    # =====================

    def open_project_dashboard(self, project_id=None):
        if project_id is None:
            project_id = self.project_selector.currentData()

        self.log.append(f"Opened Project {project_id}")

        self.project_window = ProjectDataWindow(self, project_id=project_id)
        self.project_window.exec()
        
        
    def open_treatment_dashboard(self, treatment_id=None):
        if treatment_id is None:
            treatment_id = self.treatment_selector.currentData()

        self.log.append(f"Opened Treatment {treatment_id}")

        self.treatment_window = TreatmentDataWindow(self, treatment_id=treatment_id)
        self.treatment_window.exec()