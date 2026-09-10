#!/bin/bash

DATABASE="final_ARD_projects_latest.db"

source envs/sqlitebrowser/env_sqlitebrowser.sh

sqlitebrowser "$DATABASE"