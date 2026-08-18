## Python scripts

This document lists the main Python scripts (regular scripts and GUI modules). Each entry uses a consistent structure:
- `Description:` one-line summary
- `Called by:` who calls this script
- `Imported by:` who imports this script
- `Calls:` list of Python script filenames this script calls
- `Imports:` list of Python script filenames this script imports

### scripts/python/database_to_pipeline_input.py
- Description: Assemble dataset inputs and create a pipeline run directory for a dataset.
- Called by: `scripts/shell/database_to_pipeline_input.sh`
- Imported by: none
- Calls: `1_dataset_to_analysis_files_simple_gzip_multi_threaded.py`, `2_dataset_to_manifest_file.py`, `3_dataset_to_sample_metadata.py`, `4_dataset_to_amplicon_metadata.py`, `5_dataset_symlink_files.py`, `6_dataset_directory_to_pipeline_run_directory.py`
- Imports: `create_pipeline_run.py`

### scripts/python/dataset_base_write_inputs.py
- Description: Assign base analysis units to an analysis dataset (insert/update DB rows).
- Called by: `scripts/shell/dataset_base_write_inputs.sh`
- Imported by: none
- Calls: none
- Imports: `dataset_base_make_inputs.py`

### scripts/python/0_demultiplex_primers_and_gzip.py
- Description: Demultiplex primers and gzip FASTQ files for a dataset.
- Called by: `scripts/shell/demultiplex_multiple_primers.sh`
- Imported by: none
- Calls: none (internal workflow)
- Imports: none (script-level helpers only)

### scripts/python/input_table.py
- Description: Load a TSV into a specified database table with conflict handling.
- Called by: `scripts/shell/input_table.sh`
- Imported by: none
- Calls: none
- Imports: none (only standard-library DB helpers)

### scripts/python/refresh_labels.py
- Description: Regenerate and update label fields across database tables for a project.
- Called by: `scripts/shell/refresh_labels.sh`
- Imported by: none
- Calls: none
- Imports: none (internal helpers only)

### scripts/python/update_null_au_names.py
- Description: Find and update analysis units with null names.
- Called by: `scripts/shell/update_null_au_names.sh`
- Imported by: none
- Calls: none
- Imports: none

### scripts/python/update_pipeline_run_from_snakemake.py
- Description: Parse a Snakemake-generated shell file and update pipeline_run parameters in the DB.
- Called by: `scripts/shell/update_pipeline_run_from_snakemake.sh`
- Imported by: none
- Calls: none
- Imports: none

### scripts/python/upload_pipeline_run_results_to_database.py
- Description: Load exported pipeline run results (ASVs, counts, taxonomy) into the database.
- Called by: `scripts/shell/upload_pipeline_run_results_to_database.sh`
- Imported by: none
- Calls: `upload_asvs_fasta_to_database.py`, `upload_feature_counts_to_database.py`, `upload_taxonomy_to_database.py`
- Imports: none

### scripts/python/create_pipeline_run.py
- Description: Insert a `pipeline_runs` row and return its ID.
- Called by: `database_to_pipeline_input.py`
- Imported by: `database_to_pipeline_input.py`
- Calls: none
- Imports: none

### scripts/python/db_get_columns.py
- Description: Return column names for a database table.
- Called by: GUI helpers (via imports)
- Imported by: `gui/table_matrix_add_window.py`, `gui/table_simple_add_window.py`
- Calls: none
- Imports: none

### scripts/python/db_get_data.py
- Description: DB read helpers that return pandas DataFrames for common queries.
- Called by: GUI modules (via imports)
- Imported by: `gui/general_sections.py`, `gui/main_window.py`, `gui/project_amplicon_runs_window.py`
- Calls: none
- Imports: none

### scripts/python/project_get_data.py
- Description: Project-scoped database query helpers used by GUI panels.
- Called by: GUI modules (via imports)
- Imported by: `gui/project_amplicon_runs_window.py`, `gui/project_data_window.py`, `gui/project_sections.py`
- Calls: none
- Imports: none

### scripts/python/treatment_get_data.py
- Description: Treatment-scoped database query helpers used by GUI panels.
- Called by: GUI modules (via imports)
- Imported by: `gui/treatment_sections.py`
- Calls: none
- Imports: none

### scripts/python/upload_feature_counts_to_database.py
- Description: Helper to upload feature counts for a pipeline run.
- Called by: `upload_pipeline_run_results_to_database.py`
- Imported by: none
- Calls: none
- Imports: none

### scripts/python/upload_asvs_fasta_to_database.py
- Description: Helper to upload ASV fasta sequences for a pipeline run.
- Called by: `upload_pipeline_run_results_to_database.py`
- Imported by: none
- Calls: none
- Imports: none

### scripts/python/upload_taxonomy_to_database.py
- Description: Helper to upload taxonomy assignments for a pipeline run.
- Called by: `upload_pipeline_run_results_to_database.py`
- Imported by: none
- Calls: none
- Imports: none

### Other scripts with a `main()` entry (workflow steps)
- Description: Workflow step scripts invoked by `database_to_pipeline_input.py`.
- Called by: `database_to_pipeline_input.py`
- Imported by: none
- Calls: none
- Imports: none

- `1_dataset_to_analysis_files_simple_gzip.py`
- `1_dataset_to_analysis_files_simple_gzip_multi_threaded.py`
- `2_dataset_to_manifest_file.py`
- `3_dataset_to_sample_metadata.py`
- `4_dataset_to_amplicon_metadata.py`
- `5_dataset_symlink_files.py`
- `6_dataset_directory_to_pipeline_run_directory.py`

## GUI modules (gui/)

Each GUI entry keeps the same structure for consistency.

### gui/main.py
- Description: Entry point for the Qt application.
- Called by: `scripts/shell/run_gui_main.sh`
- Imported by: none
- Calls: none
- Imports: `gui/main_window.py`

### gui/main_window.py
- Description: The main application window and tab navigation.
- Called by: `gui/main.py`
- Imported by: `gui/main.py`
- Calls: none
- Imports: `project_data_window.py`, `treatment_data_window.py`, `general_tables_data_window.py`, `db_get_data.py`

### gui/project_data_window.py
- Description: Project dashboard and data panels.
- Called by: `gui/main_window.py`
- Imported by: `gui/main_window.py`
- Calls: none
- Imports: `project_get_data.py`, `table_view_window.py`, `table_simple_add_window.py`, `table_matrix_add_window.py`, `project_sections.py`

### gui/project_sections.py
- Description: UI sections used in project views.
- Called by: GUI windows
- Imported by: `project_data_window.py`
- Calls: none
- Imports: none

### gui/project_amplicon_runs_window.py
- Description: Panel listing amplicon runs for a project.
- Called by: `project_data_window.py`
- Imported by: `project_data_window.py`
- Calls: none
- Imports: `project_get_data.py`

### gui/general_tables_data_window.py
- Description: Generic table browser for various DB tables.
- Called by: `main_window.py`
- Imported by: `main_window.py`
- Calls: none
- Imports: `general_sections.py`, `table_view_window.py`

### gui/general_sections.py
- Description: Reusable UI sections for general tables.
- Called by: GUI windows
- Imported by: `general_tables_data_window.py`
- Calls: none
- Imports: `db_get_data.py`

### gui/table_view_window.py
- Description: Dialog for viewing table contents in a copyable widget.
- Called by: other GUI windows
- Imported by: `project_data_window.py`, `treatment_data_window.py`, `general_tables_data_window.py`
- Calls: none
- Imports: `tsv_exporter.py`, `copyable_table_widget.py`

### gui/table_simple_add_window.py
- Description: Dialog for adding single-row table entries.
- Called by: GUI windows
- Imported by: `project_data_window.py`, `treatment_data_window.py`
- Calls: none
- Imports: `db_get_columns.py`, `tsv_exporter.py`

### gui/table_matrix_add_window.py
- Description: Dialog for adding matrix-style table entries.
- Called by: GUI windows
- Imported by: `project_data_window.py`
- Calls: none
- Imports: `db_get_columns.py`, `tsv_exporter.py`

### gui/treatment_data_window.py
- Description: Treatment dashboard and related tables.
- Called by: `main_window.py`
- Imported by: `main_window.py`
- Calls: none
- Imports: `treatment_sections.py`, `table_view_window.py`, `table_simple_add_window.py`

### gui/treatment_sections.py
- Description: Reusable UI sections for treatment views.
- Called by: GUI windows
- Imported by: `treatment_data_window.py`
- Calls: none
- Imports: `treatment_get_data.py`

### gui/action_box.py, gui/ui_utils.py, gui/tsv_exporter.py, gui/copyable_table_widget.py
- Description: Helper widgets and utilities used across the GUI.
- Called by: GUI windows
- Imported by: multiple GUI windows
- Calls: none
- Imports: none

