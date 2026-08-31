#!/bin/bash

## Upload input data (TSV) to a specified table in the database 

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -m scripts.python.input_table \
--table analysis_units \
--file input_staging/project_1_analysis_units_to_add.tsv \
--verbose #--no-commit
