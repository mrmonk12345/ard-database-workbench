#!/bin/bash

## Upload to database the inputs of a dataset for a given dataset_id based on the sequencing_run and amplicon_type of the dataset

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -m scripts.python.dataset_base_write_inputs --dataset-id 12 # --no-commit
