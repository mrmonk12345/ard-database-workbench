#!/bin/bash

DATABASE="final_ARD_projects_latest.db"

source /home/ARO.local/collaboration/michalm_collab/envs/sqlitebrowser/env_sqlitebrowser.sh

sqlitebrowser "$DATABASE"