"""Main window for the ARD Database graphical interface."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTabWidget, QLabel, QComboBox
)

import pandas as pd

from gui.project_data_window import ProjectDataWindow
from gui.treatment_data_window import TreatmentDataWindow
from scripts.python.db_get_data import get_projects, get_treatments


class MainWindow(QWidget):
    """Display the main application window and its navigation tabs."""

    def __init__(self):
        """Initialize the main window and create its widgets."""

        super().__init__()

        self.setWindowTitle("ARD Database GUI")

        # The main layout contains the navigation tabs and application log.
        main_layout = QVBoxLayout()

        # Create the main application tabs.
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_project_tab(), "Project")
        self.tabs.addTab(self._create_treatment_tab(), "Treatments")
        self.tabs.addTab(self._create_dataset_tab(), "Datasets")
        self.tabs.addTab(self._create_setup_tab(), "Setup")

        main_layout.addWidget(self.tabs)

        # Display status messages and user actions in a read-only log.
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

        self.setLayout(main_layout)

    # =====================
    # Tabs
    # =====================

    def _create_project_tab(self):
        """Create the project-selection tab."""

        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.project_selector = QComboBox()
        
        # Load available projects from the database.
        df = get_projects()
        
        if not df.empty:
            for _, row in df.iterrows():
                label = row["label"]

                # Show the project ID and label when a label is available.
                text = (
                    f"{row['project_id']} - {label}"
                    if pd.notna(label) and str(label).strip()
                    else str(row["project_id"])
                )
        
                self.project_selector.addItem(
                    text,
                    int(row["project_id"])
                )

        # Open the selected project when the button is clicked.
        layout.addWidget(QLabel("Select Project:"))
        layout.addWidget(self.project_selector)

        enter_btn = QPushButton("Open Project")
        enter_btn.clicked.connect(self._handle_open_project)

        layout.addWidget(enter_btn)

        return widget

    def _create_treatment_tab(self):
        """Create the treatment-selection tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.treatment_selector = QComboBox()
        
        # Load available treatments from the database.
        df = get_treatments()
        
        if not df.empty:
            for _, row in df.iterrows():
                name = row["name"]

                # Show the treatment ID and name when a name is available.
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

        # Open the selected treatment when the button is clicked.
        enter_btn = QPushButton("Open Treatment")
        enter_btn.clicked.connect(self._handle_open_treatment)

        layout.addWidget(enter_btn)

        return widget

    def _create_dataset_tab(self):
        """Create the dataset-related actions tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        export_btn = QPushButton("Export Manifest")
        export_btn.clicked.connect(self._handle_export_manifest)

        layout.addWidget(export_btn)

        return widget

    def _create_setup_tab(self):
        """Create the setup tab placeholder."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("Setup options will go here"))

        return widget

    # =====================
    # Handlers / Actions
    # =====================

    def _handle_open_project(self):
        """Open the dashboard for the selected project."""
        project_id = self.project_selector.currentData()
        self.open_project_dashboard(project_id)
    
    def _handle_open_treatment(self):
        """Open the dashboard for the selected treatment."""
        treatment_id = self.treatment_selector.currentData()
        self.open_treatment_dashboard(treatment_id)

    def _handle_export_manifest(self):
        """Log that the manifest export action was selected."""
        self.log.append("Export Manifest clicked")

    # =====================
    # Logic
    # =====================

    def open_project_dashboard(self, project_id=None):
        """Open the project data window for a selected project."""
        if project_id is None:
            project_id = self.project_selector.currentData()

        self.log.append(f"Opened Project {project_id}")

        # Keep a reference to the dialog while it is open.
        self.project_window = ProjectDataWindow(self, project_id=project_id)
        self.project_window.exec()
        
        
    def open_treatment_dashboard(self, treatment_id=None):
        """Open the treatment data window for a selected treatment."""
        if treatment_id is None:
            treatment_id = self.treatment_selector.currentData()

        self.log.append(f"Opened Treatment {treatment_id}")

        # Keep a reference to the dialog while it is open.
        self.treatment_window = TreatmentDataWindow(self, treatment_id=treatment_id)
        self.treatment_window.exec()