<img src="dep_sign.png" width=120, height=120 align="left" />

# ARD Database Docs

This folder contains an improved overview of the ARD amplicon database project. The project is a centralized system for managing metadata, sequencing data, bioinformatic analyses, and results from ARD amplicon sequencing experiments.

> Current location: this project currently lives on the ARO HPC in the michalm collaboration directory at /home/ARO.local/collaboration/michalm_collab/ARD/Projects_DB.

## What this project does

The database acts as a single source of truth for the project. It links together:

- Experimental metadata
- Biological samples and libraries
- Sequencing runs and raw FASTQ files
- Bioinformatic pipeline execution
- Analysis outputs and datasets

The main goal is to make ARD amplicon data organized, searchable, reproducible, and easy to reuse across projects.

## Why the system exists

Amplicon sequencing projects usually involve many parts. Data may come from different files, different stages of processing, and different technical contexts. This project helps keep those pieces connected so that information can be traced from the original sample to the final analysis results.

## Technology stack

The project uses a practical mix of tools:

- SQLite database
- Python
- Bash scripting
- QIIME workflows
- DB Browser for SQLite
- GUI tools for database inspection and management
- Conda environments

## Documentation set

The existing documentation was split into several files so that each topic could be covered clearly:

- database.md - database architecture, schema design, metadata philosophy, and rationale behind the data model
- tables.md - descriptions of the database tables
- workflow.md - the operational workflow for adding projects, importing data, generating pipeline inputs, running analyses, and exporting results

## Project structure

The project is organized into a few main areas:

- scripts/ - utility and processing scripts
- input_staging/ - temporary staging area for incoming table files used to add rows to the database
- gui/ - graphical user interface
- pipeline_runs/ - pipeline execution files and outputs
- raw_reads_projects/ - raw sequencing files stored by project
- analysis_files/ - analysis-ready files
- analysis_datasets/ - datasets prepared for downstream analyses

## Key files

The main database file and schema file are central to the project:

- final_ARD_projects_latest.db - the main production database
- schema.sql - database schema definition

## Typical workflow

A normal workflow usually follows these steps:

1. Open the SQLite database in a tool such as DB Browser for SQLite
2. Add or review project metadata
3. Enter sample and library information
4. Import sequencing outputs and link them to the correct records
5. Create analysis units and datasets
6. Generate pipeline inputs and run the analysis pipeline
7. Review and export the resulting tables

This structure makes the work easier to follow and easier to maintain over time.
