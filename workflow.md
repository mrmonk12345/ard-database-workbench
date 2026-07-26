# Workflow Guide

This project has a fairly clear workflow, and most of the work up to the point of creating the pipeline folder is done through DB Browser, shell scripts, and Excel files.

## Step 1: Set up the environment

Start by installing a tool for viewing and editing the SQLite database. DB Browser for SQLite is the main tool used for this project.

## Step 2: Choose the project

Pick the project you want to work on. If the project already exists, fill in any missing information. If it is new, create the project record first.

## Step 3: Add general project data

Add the core project-level data to the database. This usually includes tables such as:

- projects
- amplicon_types
- sequencing_runs
- analysis_datasets
- treatments
- locations
- rootstocks
- sampling_compartments

If relevant, treatment elements and treatment element assignments should also be added.

## Step 4: Add raw FASTQ files

Place the raw sequencing files into the project-specific directory under the raw reads area:

- raw_reads_projects/

This gives the project a physical location for its incoming files.

## Step 5: Open the GUI and inspect the project

Open the GUI and review the project before adding more data. This is a useful sanity check to make sure the database state looks right before importing new records.

The GUI can be launched from the shell scripts in the project, for example by running:

- scripts/shell/run_gui_main.sh

This is the main way to inspect tables and counts before and after imports.

## Step 6: Add samples

Use the sample import workflow to add rows to the database:

1. Open the add samples interface in the GUI
2. Choose the number of samples to add
3. Download the TSV template
4. Fill in the TSV in Excel or another spreadsheet tool
5. Save or place the file under 'input_staging/' and import it using the input table script

The relevant script is:

- scripts/shell/input_table.sh

A useful note is to close DB Browser before using the import script so that the database is not accidentally overwritten by another process.

## Step 7: Add sequencing outputs

Repeat the same general process for sequencing outputs. This step links the raw files to the relevant sequencing run and sample records.

As with samples, the workflow uses the same import route through:

- scripts/shell/input_table.sh

The data should be prepared carefully because these records connect raw files to the correct sample, project, and sequencing run.

## Step 8: Add libraries

For libraries, choose which amplicon types were used for each sample. Then download the TSV template and import the records using the same general process.

This step is important because libraries connect the sample to the sequencing target. The import is again handled through:

- scripts/shell/input_table.sh

## Step 9: Add analysis units and datasets

Repeat the process for analysis units, usually with the sequencing run information included for each library. In many cases, analysis units can be associated with datasets automatically after they are added to the database.

The project also includes scripts for creating analysis inputs, for example:

- scripts/shell/dataset_base_write_inputs.sh

This is used to assign datasets automatically after the relevant rows are inserted.

## Step 10: Clean up names and labels

Once the main data has been imported, clean up the names and labels. Useful scripts include:

- scripts/shell/update_null_au_names.sh
- scripts/shell/refresh_all_labels.sh

These scripts can affect the whole database, so it is wise to review them before running them widely.

## Step 11: Prepare the pipeline folder

To make the pipeline folder, adjust the parameters in the pipeline input script and run it. The relevant script is:

- scripts/shell/database_to_pipeline_input.sh

The first step of the pipeline often includes gzipping FASTQ files, which can be resource intensive. In some setups, this part may need to be run from a main directory or via a script that calls the relevant workflow.

pipelines will be under the directory:

- pipeline_runs/

## Step 12: Run the analysis workflow

After the pipeline folder has been prepared, the analysis can begin. Typical steps include:

- Run FastQC and MultiQC on the FASTQ files
- Use the workflow script for the desired pipeline, such as the Qiime workflow file
- Adjust the workflow script according to the amplicon type and QC settings
- Run the pipeline on the HPC system

In this project, the pipeline work is strongly tied to the generated folder structure and the input files produced by the database export scripts.

## Step 13: Export results

After analysis, export the results into simple, readable data formats. Common export steps include:

- scripts/shell/qiime_export_needed.sh
- scripts/shell/biom_export_needed.sh

These exports make the results easier to inspect, compare, and share.

## Practical advice

- Use the GUI and DB browser for inspection and manual review
- Use the scripts for batch import and repeated processing tasks
- Keep names, labels, and file paths consistent to reduce confusion
- Check that samples, libraries, sequencing outputs, and analysis units are linked correctly before running analysis

With a consistent workflow, the project becomes much easier to maintain and much easier to understand over time.
