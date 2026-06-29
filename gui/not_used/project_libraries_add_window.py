from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QWidget,
    QScrollArea, QSplitter
)
from PyQt6.QtCore import Qt

from gui.ui_utils import create_table, create_matrix_table, extract_matrix_selection

from scripts.python.project_get_data import get_project_samples
from scripts.python.project_get_data import get_project_amplicon_types
from scripts.python.project_make_libraries import make_libraries



class ProjectLibrariesAddWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle("Add Libraries")
        self.resize(1000, 650)

        main_layout = QVBoxLayout()

        # ======================
        # LOAD DATA
        # ======================
        self.samples_df = get_project_samples(project_id)
        self.samples = self.samples_df.to_dict("records")

        self.amplicons_df = get_project_amplicon_types(self.project_id)
        self.amplicons = self.amplicons_df.to_dict("records")

        # ======================
        # TOP SECTION (TABS)
        # ======================
        tabs = QTabWidget()

        # -------- TAB 1 --------
        tab1 = QWidget()
        tab1_layout = QHBoxLayout()

        # Samples table (read-only)
        samples_table = create_table(self.samples_df)
        samples_table.setEditTriggers(samples_table.EditTrigger.NoEditTriggers)

        # Amplicons table (read-only)
        amp_table = create_table(self.amplicons_df)
        amp_table.setEditTriggers(amp_table.EditTrigger.NoEditTriggers)

        tab1_layout.addWidget(samples_table)
        tab1_layout.addWidget(amp_table)

        tab1.setLayout(tab1_layout)
        tabs.addTab(tab1, "Data")

        # -------- TAB 2 (placeholder) --------
        tab2 = QWidget()
        tab2.setLayout(QVBoxLayout())
        tabs.addTab(tab2, "Other")

        # ✅ Make tabs scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tabs)

        # ======================
        # BOTTOM (MATRIX + BUTTON)
        # ======================
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()

        bottom_layout.addWidget(QLabel("Select sample / amplicon combinations"))

        self.table = create_matrix_table(
            rows_data=self.samples,
            cols_data=self.amplicons,
            row_id_key="sample_id",
            row_label_key="sample_label",
            col_id_key="amplicon_type_id"
        )

        bottom_layout.addWidget(self.table)

        btn = QPushButton("Create Libraries")
        btn.clicked.connect(self.create_libraries)
        bottom_layout.addWidget(btn)

        bottom_widget.setLayout(bottom_layout)

        # ======================
        # SPLITTER (resizable top/bottom)
        # ======================
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(scroll)         # top
        splitter.addWidget(bottom_widget)  # bottom

        splitter.setSizes([300, 400])  # initial ratio

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    # ======================
    # ACTION
    # ======================
    def create_libraries(self):
        data = extract_matrix_selection(
            table=self.table,
            rows_data=self.samples,
            cols_data=self.amplicons,
            row_id_key="sample_id",
            col_id_key="amplicon_type_id"
        )

        if not data:
            print("No selections")
            return

        make_libraries(data)

        print("Libraries created")

        self.accept()
