#!/bin/bash

## Refresh all labels in the database. Given that this is a potentially dangerous operation, it is recommended to run this script only when necessary and with caution.

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

python -c "from scripts.python.labels import refresh_all_labels; refresh_all_labels()"