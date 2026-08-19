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


