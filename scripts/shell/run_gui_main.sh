#!/bin/bash

## Run the GUI main application to view the database. also use db browser to view and edit the database tables and data.

source envs/database/env_database.sh

# keep the terminal prompt
python -m gui.main &