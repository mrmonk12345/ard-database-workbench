#!/bin/bash

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -m scripts.python.database_to_pipeline_input --dataset-id 8 --pipeline-name 'dataset_8'

