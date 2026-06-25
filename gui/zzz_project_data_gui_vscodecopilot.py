import csv
import os
import sys

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QApplication,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ImportError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QApplication,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "scripts", "python"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import project_load_samples as pls
import project_load_seqeuncing_outputs as plso
import project_make_libraries as pml
import project_make_analysis_units as pma


class ProjectDataGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ARD Project Data Entry")
        self.resize(1300, 700)

        self.db_path_edit = QLineEdit("project.db")
        self.db_path_edit.setPlaceholderText("SQLite database file path")
        self.db_path_edit.setMinimumWidth(420)
        self.db_path_edit.editingFinished.connect(self.update_db_path)

        db_browse = QPushButton("Browse DB")
        db_browse.clicked.connect(self.on_browse_db)

        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Database:"))
        db_layout.addWidget(self.db_path_edit)
        db_layout.addWidget(db_browse)
        db_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(db_layout)

        self.tabs = QTabWidget()
        self.samples_table, samples_tab = self.create_data_tab(
            "Load Samples",
            [
                "sample_name",
                "original_sample_label",
                "sample_label",
                "project_id",
                "initial_health_status",
                "final_health_status",
                "location_id",
                "rootstock_id",
                "sampling_compartment_id",
                "treatment_id",
                "time_since_planting",
                "host_species",
                "scion_cultivar",
                "soil_texture",
                "soil_type",
                "sampling_depth",
                "experimental_setting",
            ],
            submit_label="Load Samples",
            submit_action=self.on_submit_samples,
        )

        self.seq_outputs_table, seq_outputs_tab = self.create_data_tab(
            "Load Sequencing Outputs",
            [
                "sequencing_output_label",
                "project_id",
                "sample_id",
                "sequencing_run_id",
                "amplicon_type_id",
                "srr",
                "fastq1",
                "fastq2",
                "notes",
            ],
            submit_label="Load Sequencing Outputs",
            submit_action=self.on_submit_seq_outputs,
        )

        self.libraries_table, libraries_tab = self.create_data_tab(
            "Make Libraries",
            ["Use", "sample_id", "amplicon_type_ids"],
            submit_label="Make Libraries",
            submit_action=self.on_submit_libraries,
            checkbox_column=0,
        )

        self.analysis_units_table, analysis_units_tab = self.create_data_tab(
            "Make Analysis Units",
            ["Use", "library_id", "sequencing_run_ids"],
            submit_label="Make Analysis Units",
            submit_action=self.on_submit_analysis_units,
            checkbox_column=0,
        )

        self.tabs.addTab(samples_tab, "Load Samples")
        self.tabs.addTab(seq_outputs_tab, "Load Sequencing Outputs")
        self.tabs.addTab(libraries_tab, "Make Libraries")
        self.tabs.addTab(analysis_units_tab, "Make Analysis Units")

        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.update_db_path()

    def create_data_tab(self, title, columns, submit_label, submit_action, checkbox_column=None):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget(0, len(columns), self)
        table.setHorizontalHeaderLabels(columns)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)

        buttons_layout = QHBoxLayout()
        add_row_btn = QPushButton("Add Row")
        add_row_btn.clicked.connect(lambda: self.add_row(table, checkbox_column))
        remove_row_btn = QPushButton("Remove Selected")
        remove_row_btn.clicked.connect(lambda: self.remove_selected_rows(table))
        load_csv_btn = QPushButton("Load CSV")
        load_csv_btn.clicked.connect(lambda: self.load_csv(table, columns, checkbox_column))
        save_csv_btn = QPushButton("Save CSV")
        save_csv_btn.clicked.connect(lambda: self.save_csv(table, columns, checkbox_column))
        submit_btn = QPushButton(submit_label)
        submit_btn.clicked.connect(submit_action)

        buttons_layout.addWidget(add_row_btn)
        buttons_layout.addWidget(remove_row_btn)
        buttons_layout.addWidget(load_csv_btn)
        buttons_layout.addWidget(save_csv_btn)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(submit_btn)

        layout.addLayout(buttons_layout)
        layout.addWidget(table)
        layout.setContentsMargins(8, 8, 8, 8)
        return table, widget

    def on_browse_db(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select SQLite DB", os.getcwd(), "SQLite Files (*.db *.sqlite);;All Files (*)")
        if path:
            self.db_path_edit.setText(path)
            self.update_db_path()

    def update_db_path(self):
        db_path = self.db_path_edit.text().strip() or "project.db"
        for module in (pls, plso, pml, pma):
            module.DB_PATH = db_path

    def add_row(self, table, checkbox_column=None):
        row = table.rowCount()
        table.insertRow(row)
        for col in range(table.columnCount()):
            if col == checkbox_column:
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked)
            else:
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            table.setItem(row, col, item)

    def remove_selected_rows(self, table):
        selected = sorted({index.row() for index in table.selectedIndexes()}, reverse=True)
        for row in selected:
            table.removeRow(row)

    def load_csv(self, table, columns, checkbox_column=None):
        path, _ = QFileDialog.getOpenFileName(self, "Load CSV", os.getcwd(), "CSV Files (*.csv);;All Files (*)")
        if not path:
            return
        with open(path, newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            table.setRowCount(0)
            for row in reader:
                row_index = table.rowCount()
                table.insertRow(row_index)
                for col, header in enumerate(columns):
                    if checkbox_column is not None and col == checkbox_column:
                        item = QTableWidgetItem()
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        item.setCheckState(Qt.Checked)
                    else:
                        item = QTableWidgetItem(row.get(header, ""))
                        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
                    table.setItem(row_index, col, item)

    def save_csv(self, table, columns, checkbox_column=None):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", os.getcwd(), "CSV Files (*.csv);;All Files (*)")
        if not path:
            return
        headers = [col for col in columns if col != "Use"]
        with open(path, "w", newline="", encoding="utf-8") as dest:
            writer = csv.DictWriter(dest, fieldnames=headers)
            writer.writeheader()
            for row in range(table.rowCount()):
                row_data = {}
                skip = False
                for col, header in enumerate(columns):
                    item = table.item(row, col)
                    if checkbox_column is not None and col == checkbox_column:
                        if item.checkState() != Qt.Checked:
                            skip = True
                        continue
                    row_data[header] = item.text() if item is not None else ""
                if not skip:
                    writer.writerow(row_data)

    def read_table_data(self, table, field_names, checkbox_column=None, list_fields=None):
        list_fields = list_fields or []
        items = []
        for row in range(table.rowCount()):
            if checkbox_column is not None:
                checkbox_item = table.item(row, checkbox_column)
                if checkbox_item is None or checkbox_item.checkState() != Qt.Checked:
                    continue
            row_data = {}
            for col, field in enumerate(field_names):
                if checkbox_column is not None and col == checkbox_column:
                    continue
                item = table.item(row, col)
                value = item.text().strip() if item is not None else ""
                if field in list_fields:
                    row_data[field] = self.parse_list_field(value)
                else:
                    row_data[field] = value
            items.append(row_data)
        return items

    def parse_list_field(self, text):
        return [value.strip() for value in text.split(",") if value.strip()]

    def on_submit_samples(self):
        data = self.read_table_data(
            self.samples_table,
            [
                "sample_name",
                "original_sample_label",
                "sample_label",
                "project_id",
                "initial_health_status",
                "final_health_status",
                "location_id",
                "rootstock_id",
                "sampling_compartment_id",
                "treatment_id",
                "time_since_planting",
                "host_species",
                "scion_cultivar",
                "soil_texture",
                "soil_type",
                "sampling_depth",
                "experimental_setting",
            ],
        )
        if not data:
            self.show_message("No Samples", "No sample rows were provided.")
            return
        try:
            pls.load_samples(data)
            self.show_message("Success", f"Loaded {len(data)} sample row(s) into the database.")
        except Exception as exc:
            self.show_message("Error Loading Samples", str(exc), error=True)

    def on_submit_seq_outputs(self):
        data = self.read_table_data(
            self.seq_outputs_table,
            [
                "sequencing_output_label",
                "project_id",
                "sample_id",
                "sequencing_run_id",
                "amplicon_type_id",
                "srr",
                "fastq1",
                "fastq2",
                "notes",
            ],
        )
        if not data:
            self.show_message("No Sequencing Outputs", "No sequencing output rows were provided.")
            return
        try:
            plso.load_sequencing_outputs(data)
            self.show_message("Success", f"Loaded {len(data)} sequencing output row(s) into the database.")
        except Exception as exc:
            self.show_message("Error Loading Sequencing Outputs", str(exc), error=True)

    def on_submit_libraries(self):
        data = self.read_table_data(
            self.libraries_table,
            ["Use", "sample_id", "amplicon_type_ids"],
            checkbox_column=0,
            list_fields=["amplicon_type_ids"],
        )
        if not data:
            self.show_message("No Libraries", "No library rows were selected for creation.")
            return
        try:
            pml.make_libraries(data)
            self.show_message("Success", f"Processed {len(data)} library row(s).")
        except Exception as exc:
            self.show_message("Error Making Libraries", str(exc), error=True)

    def on_submit_analysis_units(self):
        data = self.read_table_data(
            self.analysis_units_table,
            ["Use", "library_id", "sequencing_run_ids"],
            checkbox_column=0,
            list_fields=["sequencing_run_ids"],
        )
        if not data:
            self.show_message("No Analysis Units", "No analysis unit rows were selected for creation.")
            return
        try:
            pma.make_analysis_units(data)
            self.show_message("Success", f"Processed {len(data)} analysis unit row(s).")
        except Exception as exc:
            self.show_message("Error Making Analysis Units", str(exc), error=True)

    def show_message(self, title, text, error=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical if error else QMessageBox.Information)
        msg.exec()


def main():
    app = QApplication(sys.argv)
    window = ProjectDataGui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
