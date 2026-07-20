from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt

from gui.table_view_window import TableViewWindow
from gui.project_table_simple_add_window import ProjectTableSimpleAddWindow

from scripts.python.treatment_get_data import (
    get_treatment_element_assignments,
    get_treatment_elements,
    get_treatment_samples,
    get_treatment_projects,
    get_treatment_element_assignments_count,
    get_treatment_elements_count,
    get_treatment_samples_count,
    get_treatment_projects_count,
)


class TreatmentDataWindow(QDialog):
    def __init__(self, parent=None, treatment_id=None):
        super().__init__(parent)

        self.treatment_id = treatment_id

        self.setWindowTitle(f"Treatment Data - {self.treatment_id}")
        self.resize(500, 500)

        self.counts = {
            "assignments": get_treatment_element_assignments_count(self.treatment_id),
            "elements" : get_treatment_elements_count(self.treatment_id),
            "samples": get_treatment_samples_count(self.treatment_id),
            "projects": get_treatment_projects_count(self.treatment_id),
        }

        layout = QVBoxLayout(self)

        layout.addWidget(self._assignments_box())
        layout.addWidget(self._elements_box())
        layout.addWidget(self._samples_box())
        layout.addWidget(self._projects_box())

    # =====================
    # Helpers
    # =====================

    def _create_count_label(self, count):
        lbl = QLabel(str(count))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        return lbl

    def _create_action_box(self, title, count, view_func, add_func=None):
        box = QGroupBox(title)

        layout = QVBoxLayout()
        layout.addWidget(self._create_count_label(count))

        btn_layout = QHBoxLayout()

        view_btn = QPushButton(f"View {title}")
        view_btn.clicked.connect(view_func)
        btn_layout.addWidget(view_btn)

        if add_func:
            add_btn = QPushButton(f"Add {title}")
            add_btn.clicked.connect(add_func)
            btn_layout.addWidget(add_btn)

        layout.addLayout(btn_layout)
        box.setLayout(layout)

        return box

    # =====================
    # Boxes
    # =====================

    def _assignments_box(self):
        return self._create_action_box(
            title="Treatment Assignments",
            count=self.counts["assignments"],
            view_func=self.open_assignments_view,
            add_func=self.open_assignments_add
        )

    def _elements_box(self):
        return self._create_action_box(
            title="Treatment Elements",
            count=self.counts["elements"],
            view_func=self.open_elements_view,
            add_func=self.open_elements_add
        )

    def _samples_box(self):
        return self._create_action_box(
            title="Samples",
            count=self.counts["samples"],
            view_func=self.open_samples_view
        )

    def _projects_box(self):
        return self._create_action_box(
            title="Projects",
            count=self.counts["projects"],
            view_func=self.open_projects_view
        )

    # =====================
    # Views
    # =====================

    def open_assignments_view(self):
        self.window = TableViewWindow(
        self,
        entity_id=self.treatment_id,
        table_name="Treatment Element Assignments",
        get_data_func=get_treatment_element_assignments,
        output_filename=f"treatment_{self.treatment_id}_assignments.tsv",
        )
        self.window.show()

    def open_elements_view(self):
        self.window = TableViewWindow(
        self,
        entity_id=self.treatment_id,
        table_name="Treatment Elements",
        get_data_func=get_treatment_elements,
        output_filename=f"treatment_{self.treatment_id}_elements.tsv",
        )
        self.window.show()

    def open_samples_view(self):
        self.window = TableViewWindow(
            self,
            entity_id=self.treatment_id,
            table_name="Samples",
            get_data_func=get_treatment_samples,
            output_filename=f"treatment_{self.treatment_id}_samples.tsv"
        )
        self.window.show()

    def open_projects_view(self):
        self.window = TableViewWindow(
            self,
            entity_id=self.treatment_id,
            table_name="Projects",
            get_data_func=get_treatment_projects,
            output_filename=f"treatment_{self.treatment_id}_projects.tsv"
        )
        self.window.show()

    # =====================
    # Add
    # =====================

    def open_assignments_add(self):
        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=None,
            table_name="treatment_assignments",
            pk_column="treatment_assignment_id",
            output_filename=f"treatment_{self.treatment_id}_assignments_to_add.tsv"
        )
        self.window.show()

    def open_elements_add(self):
        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=None,
            table_name="treatment_elements",
            pk_column="treatment_element_id",
            output_filename=f"treatment_{self.treatment_id}_elements_to_add.tsv"
        )
        self.window.show()