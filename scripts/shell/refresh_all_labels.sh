#!/bin/bash

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -c "from scripts.python.labels import refresh_all_labels; refresh_all_labels()"