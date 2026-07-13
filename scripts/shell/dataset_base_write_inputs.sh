#!/bin/bash

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -m scripts.python.dataset_base_write_inputs --dataset-id 9  --no-commit
