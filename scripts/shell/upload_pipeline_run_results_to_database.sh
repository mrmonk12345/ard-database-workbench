#!/bin/bash

## upload to database the results of a pipeline run for a given pipeline_run_id

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python  -m scripts.python.upload_pipeline_run_results_to_database --pipeline-run-id 8
