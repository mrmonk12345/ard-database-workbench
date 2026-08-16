#!/bin/bash

## Create pipeline_run input from selected dataset directory for a given dataset_id

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -m scripts.python.database_to_pipeline_input --dataset-id 10 --no-step-1

