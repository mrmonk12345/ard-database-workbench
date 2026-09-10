#!/bin/bash

## Refresh all labels in the database. Given that this is a potentially dangerous operation, it is recommended to run this script only when necessary and with caution.

source envs/database/env_database.sh

python -m scripts.python.refresh_labels --project-id 1
