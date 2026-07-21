from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
)

from gui.action_box import ActionBox
from gui.table_view_window import TableViewWindow
from gui.table_simple_add_window import TableSimpleAddWindow

from gui.treatment_sections import (
    assignments_section,
    elements_section,
    samples_section,
    projects_section,
)

#from gui.simple_add_window import SimpleAddWindow


class TreatmentDataWindow(QDialog):

    def __init__(
        self,
        parent=None,
        treatment_id=None,
    ):
        super().__init__(parent)

        self.treatment_id = treatment_id

        self.setWindowTitle(
            f"Treatment Data - {treatment_id}"
        )

        self.resize(600, 500)

        layout = QVBoxLayout(self)

        sections = [

            assignments_section(self),

            elements_section(self),

            samples_section(self),

            projects_section(self),
        ]

        for section in sections:

            layout.addWidget(
                ActionBox(
                    title=section["title"],
                    count=section["count"],
                    buttons=section["buttons"],
                )
            )

    # ==================================
    # Generic table opener
    # ==================================

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

    # ==================================
    # Add windows
    # ==================================
    def open_assignments_add(self): 
        self.window = TableSimpleAddWindow(
            self,
            entity_id=self.treatment_id,
            entity_column="treatment_id",
            table_name="treatment_element_assignments",
            pk_column="treatment_assignment_id",
            output_filename=f"treatment_{self.treatment_id}_assignments_to_add.tsv",
        )

        self.window.show()

    def open_elements_add(self):
        self.window = TableSimpleAddWindow(
            self,
            entity_id=self.treatment_id,
            entity_column="treatment_id",
            table_name="treatment_elements",
            pk_column="treatment_element_id",
            output_filename=f"treatment_{self.treatment_id}_elements_to_add.tsv",
        )

        self.window.show()