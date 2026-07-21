from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QWidget,
    QScrollArea,
)

from gui.action_box import ActionBox
from gui.table_view_window import TableViewWindow

from gui.project_sections import *

from gui.project_table_simple_add_window import (
    ProjectTableSimpleAddWindow
)

from gui.project_table_matrix_add_window import (
    ProjectTableMatrixAddWindow
)

from scripts.python.project_get_data import (
    get_project_samples,
    get_project_amplicon_types,
    get_project_libraries,
    get_project_sequencing_runs,
    get_project_sequencing_runs_count,
    get_project_amplicon_types_count,
)


class ProjectDataWindow(QDialog):

    def __init__(
        self,
        parent=None,
        project_id=None,
    ):
        super().__init__(parent)

        self.project_id = project_id

        self.setWindowTitle(
            f"Project Data - {project_id}"
        )

        self.resize(600, 900)

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout(content)

        top = QHBoxLayout()

        top.addWidget(
            self.display_box(
                "Sequencing Runs",
                get_project_sequencing_runs_count(
                    project_id
                )
            )
        )

        top.addWidget(
            self.display_box(
                "Amplicon Types",
                get_project_amplicon_types_count(
                    project_id
                )
            )
        )

        layout.addLayout(top)

        btn = QPushButton(
            "View Sequencing Runs & Amplicon Types"
        )

        btn.clicked.connect(
            self.open_runs_amplicon
        )

        layout.addWidget(btn)

        sections = [

            samples_section(self),

            outputs_section(self),

            libraries_section(self),

            analysis_units_section(self),

            analysis_unit_files_section(self),

            analysis_datasets_section(self),

            analysis_dataset_inputs_section(self),

            pipeline_runs_section(self),
        ]

        for section in sections:

            layout.addWidget(
                ActionBox(
                    title=section["title"],
                    count=section["count"],
                    buttons=section["buttons"],
                )
            )

        scroll.setWidget(content)

        main_layout.addWidget(scroll)

    def display_box(
        self,
        title,
        count,
    ):
        box = QGroupBox(title)

        layout = QVBoxLayout()

        label = QLabel(str(count))

        label.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        layout.addWidget(label)

        box.setLayout(layout)

        return box

    def open_table(
        self,
        table_name,
        dataframe,
        filename,
    ):
        self.window = TableViewWindow(
            self,
            dataframe=dataframe,
            table_name=table_name,
            output_filename=filename,
        )

        self.window.show()

    def open_samples_add(self):

        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=self.project_id,
            table_name="samples",
            pk_column="sample_id",
            output_filename=f"project_{self.project_id}_samples_to_add.tsv"
        )

        self.window.show()

    def open_outputs_add(self):

        self.window = ProjectTableSimpleAddWindow(
            self,
            project_id=self.project_id,
            table_name="sequencing_outputs",
            pk_column="sequencing_output_id",
            output_filename=f"project_{self.project_id}_sequencing_outputs_to_add.tsv"
        )

        self.window.show()

    def open_libraries_add(self):

        samples = get_project_samples(
            self.project_id
        ).to_dict("records")

        amplicons = get_project_amplicon_types(
            self.project_id
        ).to_dict("records")

        self.window = ProjectTableMatrixAddWindow(
            self,
            project_id=self.project_id,
            table_name="libraries",
            pk_column="library_id",
            rows_data=samples,
            cols_data=amplicons,
            row_id_key="sample_id",
            row_label_key="label",
            col_id_key="amplicon_type_id",
            output_filename=f"project_{self.project_id}_libraries_to_add.tsv"
        )

        self.window.show()

    def open_analysis_units_add(self):

        libraries = get_project_libraries(
            self.project_id
        ).to_dict("records")

        runs = get_project_sequencing_runs(
            self.project_id
        ).to_dict("records")

        self.window = ProjectTableMatrixAddWindow(
            self,
            project_id=self.project_id,
            table_name="analysis_units",
            pk_column="analysis_unit_id",
            rows_data=libraries,
            cols_data=runs,
            row_id_key="library_id",
            row_label_key="label",
            col_id_key="sequencing_run_id",
            output_filename=f"project_{self.project_id}_analysis_units_to_add.tsv"
        )

        self.window.show()

    def open_runs_amplicon(self):

        from gui.project_amplicon_runs_window import (
            ProjectAmpliconRunsWindow
        )

        self.window = ProjectAmpliconRunsWindow(
            self,
            project_id=self.project_id
        )

        self.window.show()