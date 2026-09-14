# Shell scripts

This document lists the convenience shell scripts in `scripts/shell/`, a short description of what each does, and the Python module each script invokes.

## scripts/shell/database_to_pipeline_input.sh

- Description: Create pipeline_run input from a selected dataset directory for a given `dataset_id`.
- Calls: [scripts/python/database_to_pipeline_input.py](scripts/python/database_to_pipeline_input.py)
- Invoked as: `python -m scripts.python.database_to_pipeline_input`

## scripts/shell/dataset_base_write_inputs.sh

- Description: Upload dataset inputs to the database for a given `dataset_id` (based on sequencing_run and amplicon_type).
- Calls: [scripts/python/dataset_base_write_inputs.py](scripts/python/dataset_base_write_inputs.py)
- Invoked as: `python -m scripts.python.dataset_base_write_inputs`

## scripts/shell/demultiplex_multiple_primers.sh

- Description: Demultiplex primers and gzip results for a dataset (wraps the demultiplexing pipeline step).
- Calls: [scripts/python/0_demultiplex_primers_and_gzip.py](scripts/python/0_demultiplex_primers_and_gzip.py)
- Invoked as: `python -m scripts.python.0_demultiplex_primers_and_gzip`

## scripts/shell/export_tables.sh

- Description: Export selected database tables using the queries configured in `export_tables.py`.
- Calls: `export_tables.py`
- Invoked as: `python -m export_tables`

## scripts/shell/input_table.sh

- Description: Upload a TSV file into a specified database table (convenience wrapper around the input table uploader).
- Calls: [scripts/python/input_table.py](scripts/python/input_table.py)
- Invoked as: `python -m scripts.python.input_table`

## scripts/shell/refresh_labels.sh

- Description: Refresh labels in the database. This is a potentially dangerous operation — run with caution.
- Calls: [scripts/python/refresh_labels.py](scripts/python/refresh_labels.py)
- Invoked as: `python -m scripts.python.refresh_labels`

## scripts/shell/run_gui_main.sh

- Description: Launch the graphical UI for browsing and editing the database.
- Calls: [gui/main.py](gui/main.py) by running the module `gui.main`.
- Invoked as: `python -m gui.main`

## scripts/shell/run_sqlitebrowser.sh

- Description: Open the SQLite database in SQLite Browser.
- Calls: none
- Invoked as: `sqlitebrowser final_ARD_projects_latest.db`

## scripts/shell/update_null_au_names.sh

- Description: Update analysis units that have null names in the database. Use with caution.
- Calls: [scripts/python/update_null_au_names.py](scripts/python/update_null_au_names.py)
- Invoked as: `python -m scripts.python.update_null_au_names`

## scripts/shell/update_pipeline_run_from_snakemake.sh

- Description: Update a `pipeline_run` record in the database using parameters from a Snakemake run.
- Calls: [scripts/python/update_pipeline_run_from_snakemake.py](scripts/python/update_pipeline_run_from_snakemake.py)
- Invoked as: `python -m scripts.python.update_pipeline_run_from_snakemake`

## scripts/shell/upload_pipeline_run_results_to_database.sh

- Description: Upload results produced by a pipeline run into the database for a given `pipeline_run_id`.
- Calls: [scripts/python/upload_pipeline_run_results_to_database.py](scripts/python/upload_pipeline_run_results_to_database.py)
- Invoked as: `python -m scripts.python.upload_pipeline_run_results_to_database`

## scripts/shell/upload_taxonomy_pipeline_results_to_database.sh

- Description: Upload taxonomy results for a pipeline run into the database.
- Calls: [scripts/python/upload_taxonomy_to_database.py](scripts/python/upload_taxonomy_to_database.py)
- Invoked as: `python scripts/python/upload_taxonomy_to_database.py --pipeline-run-id <id> --reference <reference> --taxonomy <file> --db-path <database>`

## Pipeline-run shell scripts

The example pipeline scripts are stored in
[pipeline_runs/example_pipeline](pipeline_runs/example_pipeline). They are run from the
pipeline-run directory and use the HPC QIIME 2 and Snakemake environments.

- `hpc.sh` is the HPC launcher and calls `snakemake_qiime.sh`.
- `snakemake_qiime.sh` loads the QIIME 2 and Snakemake environments, defines the run parameters,
  and contains the workflow commands.
- `fastqc.sh`, `multiqc.sh`, and `run_all_qc.sh` run quality-control steps.
- `qiime_export_needed.sh` and `biom_export_needed.sh` export selected results.
- `run_gtdb_pipeline.sh`, `run_silva_pipeline.sh`, and
	`run_gtdb_classification_pretrained.sh` run taxonomy-related pipeline steps.

Read [the example pipeline README](pipeline_runs/example_pipeline/README.md) before adapting
these scripts for a new pipeline run. They contain project-specific parameters and should be
reviewed before execution.

## Classifier shell scripts

The reference-data scripts are stored in
[pipeline_runs/classifiers](pipeline_runs/classifiers). `rescript_silva.sh` prepares SILVA
reference files, while `rescript_gtdb.sh` prepares GTDB reference files. Both require the HPC
QIIME 2 environment and create `.qza` files used by taxonomy workflows.

See [the classifiers README](pipeline_runs/classifiers/README.md) for the inputs, outputs, and
version settings to review before running them.


