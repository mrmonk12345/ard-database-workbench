#!/bin/bash

## Update a pipeline_run in the database based on the parameters in the snakemake script.

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python  -m scripts.python.update_pipeline_run_from_snakemake --pipeline-run-id 2 
