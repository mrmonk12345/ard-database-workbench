from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel

from scripts.python.project_get_data import get_project_samples
from scripts.python.db_get_data import get_amplicon_types

from scripts.python.project_make_libraries import make_libraries

from gui.libraries_utils import (
    create_libraries_table,
    extract_sample_amplicons
)


class ProjectLibrariesAddWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle("Add Libraries")
        self.resize(900, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select sample / amplicon combinations"))

        # ✅ load data
        self.samples = get_project_samples(project_id).to_dict("records")
        self.amplicons = get_amplicon_types().to_dict("records")

        # ✅ create matrix table
        self.table = create_libraries_table(self.samples, self.amplicons)
        layout.addWidget(self.table)

        # ✅ button
        btn = QPushButton("Create Libraries")
        btn.clicked.connect(self.create_libraries)
        layout.addWidget(btn)

        self.setLayout(layout)

    # ======================
    # ACTION
    # ======================
    def create_libraries(self):
        data = extract_sample_amplicons(
            self.table,
            self.samples,
            self.amplicons
        )

        if not data:
            print("No selections")
            return

        make_libraries(data)

        print("Libraries created")

        self.accept()