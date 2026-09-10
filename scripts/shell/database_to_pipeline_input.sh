#!/bin/bash

## Create pipeline_run input from selected dataset directory for a given dataset_id

source envs/database/env_database.sh

python -m scripts.python.database_to_pipeline_input --dataset-id 4 --pipeline-run-id 5  #--no-step-1

