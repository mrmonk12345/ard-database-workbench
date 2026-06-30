from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import Qt

# ✅ New generic windows
from gui.project_table_view_window import ProjectTableViewWindow
from gui.project_table_simple_add_window import ProjectTableSimpleAddWindow
from gui.project_table_matrix_add_window import ProjectTableMatrixAddWindow

# ✅ Data loaders
from scripts.python.project_get_data import (
    get_project_samples,
    get_project_amplicon_types,
    get_project_sequencing_outputs,
    get_project_libraries,
    get_project_analysis_units,
    get_project_sequencing_runs
)

from scripts.python.project_get_data import (
    get_project_sequencing_runs_count,
    get_project_amplicon_types_count,
    get_project_samples_count,
    get_project_sequencing_outputs_count,
    get_project_libraries_count,
    get_project_analysis_units_count
)


class ProjectDataWindow(QDialog):
    def __init__(self, parent=None, project_id=None):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle(f"Project Data - {self.project_id}")
        self.resize(500, 700)

        layout = QVBoxLayout()

        # =====================
        # Load counts
        # =====================
        self.counts = self._load_counts()

        # =====================
        # Top section
        # =====================
        top = QHBoxLayout()
        top.addWidget(self._create_display_box("Sequencing Runs", self.counts["runs"]))
        top.addWidget(self._create_display_box("Amplicon Types", self.counts["amplicon"]))
        layout.addLayout(top)

        # Combined button (keep as-is if still needed)
        btn = QPushButton("View Sequencing Runs & Amplicon Types")
        btn.clicked.connect(self.open_runs_amplicon)
        layout.addWidget(btn)

        # =====================
        # Sections
        # =====================
        layout.addWidget(self._samples_box())
        layout.addWidget(self._outputs_box())
        layout.addWidget(self._libraries_box())
        layout.addWidget(self._analysis_units_box())

        self.setLayout(layout)

    # =====================
    # Data
    # =====================

    def _load_counts(self):
        return {
            "runs": get_project_sequencing_runs_count(self.project_id),
            "amplicon": get_project_amplicon_types_count(self.project_id),
            "samples": get_project_samples_count(self.project_id),
            "outputs": get_project_sequencing_outputs_count(self.project_id),
            "libraries": get_project_libraries_count(self.project_id),
            "analysis_units": get_project_analysis_units_count(self.project_id),
        }

    # =====================
    # UI helpers
    # =====================

    def _create_count_label(self, count):
        lbl = QLabel(str(count))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        return lbl

    def _create_display_box(self, title, count):
        box = QGroupBox(title)
        layout = QVBoxLayout()
        layout.addWidget(self._create_count_label(count))
        box.setLayout(layout)
        return box

    # =====================
    # BOXES (NEW STYLE)
    # =====================

    def _samples_box(self):
        return self._create_action_box(
            title="Samples",
            count=self.counts["samples"],
            view_func=self.open_samples_view,
            add_func=self.open_samples_add
        )

    def _outputs_box(self):
        return self._create_action_box(
            title="Sequencing Outputs",
            count=self.counts["outputs"],
            view_func=self.open_outputs_view,
            add_func=self.open_sequencing_outputs_add
        )

    def _libraries_box(self):
        return self._create_action_box(
            title="Libraries",
            count=self.counts["libraries"],
            view_func=self.open_libraries_view,
            add_func=self.open_libraries_add
        )

    def _analysis_units_box(self):
        return self._create_action_box(
            title="Analysis Units",
            count=self.counts["analysis_units"],
            view_func=self.open_analysis_units_view,
            add_func=self.open_analysis_units_add
        )

    def _create_action_box(self, title, count, view_func, add_func):
        box = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addWidget(self._create_count_label(count))

        btn_layout = QHBoxLayout()

        # ✅ View
        view_btn = QPushButton(f"View {title}")
        view_btn.clicked.connect(view_func)
        btn_layout.addWidget(view_btn)

        # ✅ Add
        if add_func:
            add_btn = QPushButton(f"Add {title}")
            add_btn.clicked.connect(add_func)
            btn_layout.addWidget(add_btn)

        layout.addLayout(btn_layout)
        box.setLayout(layout)

        return box

    # =====================
    # VIEW WINDOWS
    # =====================

    def open_samples_view(self):
        self.window = ProjectTableViewWindow(
            self,
            project_id=self.project_id,
            table_name="Samples",
            get_data_func=get_project_samples,
            output_filename=f"project_{self.project_id}_samples.tsv"
        )
        self.window.show()

    def open_outputs_view(self):
        self.window = ProjectTableViewWindow(
            self,
            project_id=self.project_id,
            table_name="Sequencing Outputs",
            get_data_func=get_project_sequencing_outputs,
            output_filename=f"project_{self.project_id}_sequencing_outputs.tsv"
        )
        self.window.show()

    def open_libraries_view(self):
        self.window = ProjectTableViewWindow(
            self,
            project_id=self.project_id,
            table_name="Libraries",
            get_data_func=get_project_libraries,
            output_filename=f"project_{self.project_id}_libraries.tsv"
        )
        self.window.show()

    def open_analysis_units_view(self):
        self.window = ProjectTableViewWindow(
            self,
            project_id=self.project_id,
            table_name="Analysis Units",
            get_data_func=get_project_analysis_units,
            output_filename=f"project_{self.project_id}_analysis_units.tsv"
        )
        self.window.show()

    # =====================
    # ADD WINDOWS
    # =====================

    def open_samples_add(self):
        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=self.project_id,
            table_name="samples",
            pk_column="sample_id",
            output_filename=f"project_{self.project_id}_samples_to_add.tsv"
        )
        self.window.show()
    
    def open_sequencing_outputs_add(self):
        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=self.project_id,
            table_name="sequencing_outputs",
            pk_column="sequencing_output_id",
            output_filename=f"project_{self.project_id}_sequencing_outputs_to_add.tsv"
        )
        self.window.show()

    def open_libraries_add(self):
        samples = get_project_samples(self.project_id).to_dict("records")
        amplicons = get_project_amplicon_types(self.project_id).to_dict("records")

        self.window = ProjectTableMatrixAddWindow(
            self,
            project_id=self.project_id,
            table_name="libraries",
            pk_column="library_id",
            rows_data=samples,
            cols_data=amplicons,
            row_id_key="sample_id",
            row_label_key="sample_label",
            col_id_key="amplicon_type_id",
            output_filename=f"project_{self.project_id}_libraries_to_add.tsv"
        )
        self.window.show()
    
    def open_analysis_units_add(self):
        libraries = get_project_libraries(self.project_id).to_dict("records")
        sequencing_runs = get_project_sequencing_runs(self.project_id).to_dict("records")
        self.window = ProjectTableMatrixAddWindow(
            self,
            project_id=self.project_id,
            table_name="analysis_units",
            pk_column="analysis_unit_id",
            rows_data=libraries,
            cols_data=sequencing_runs,
            row_id_key="library_id",
            row_label_key="library_label",
            col_id_key="sequencing_run_id",
            output_filename=f"project_{self.project_id}_analysis_units_to_add.tsv"
        )
        self.window.show()

    # =====================
    # EXISTING
    # =====================

    def open_runs_amplicon(self):
        from gui.project_amplicon_runs_window import ProjectAmpliconRunsWindow
        self.window = ProjectAmpliconRunsWindow(self, project_id=self.project_id)
        self.window.show()
