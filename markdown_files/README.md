# ARD Amplicon Database

## Overview

The ARD Amplicon Database is a centralized platform for managing metadata, sequencing data, bioinformatic analyses, and results generated from ARD amplicon sequencing experiments.

The project serves as a single source of truth that links:

* Experimental metadata
* Biological samples and libraries
* Sequencing runs and raw FASTQ files
* Bioinformatic pipeline execution
* Analysis outputs and datasets

The goal is to make ARD amplicon data organized, searchable, reproducible, and easily reusable across multiple projects.



## Technology Stack

* SQLite database
* Python
* Bash scripting
* QIIME workflows
* DB Browser for SQLite
* GUI tools for database inspection and management
* Conda environments



## Documentation

Detailed documentation is kept separate from this README:

* database\_design.md – database architecture, schema design, metadata philosophy, and rationale behind the data model.
* database_tables_explanation.md – detailed description of all database tables
* workflow.md – detailed operational workflow for adding projects, importing data, generating pipeline inputs, running analyses, and exporting results.



## Project Structure

|Directory|Purpose|
|-|-|
|scripts/|Utility and processing scripts|
|raw\_reads\_projects/|Raw sequencing data and project inputs|
|pipeline\_runs/|Pipeline execution files and outputs|
|input\_staging/|Temporary staging area for incoming data|
|gui/|Graphical user interface|
|articles/|Reference literature|
|analysis\_files/|Analysis-ready files|
|analysis\_datasets/|Datasets prepared for downstream analyses|
|not\_used/|Archived or unused files|



## Key Files

|File|Description|
|-|-|
|final\_ARD\_projects\_latest.db|Main production database|


