#!/bin/bash

## Update a pipeline_run in the database based on the parameters in the snakemake script.

source envs/database/env_database.sh

python  -m scripts.python.update_pipeline_run_from_snakemake --pipeline-run-id 9 
