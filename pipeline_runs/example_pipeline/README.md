# Example pipeline

This directory contains an example QIIME 2 and Snakemake pipeline layout. It is a template
for pipeline runs, not a replacement for the project-specific input files and parameters.

## Main shell scripts

- `hpc.sh` is the HPC launcher; it calls `snakemake_qiime.sh`.
- `snakemake_qiime.sh` loads the QIIME 2 and Snakemake environments, defines the run parameters,
  and contains the workflow commands.
- `run_all_qc.sh`, `fastqc.sh`, and `multiqc.sh` run quality-control steps.
- `qiime_export_needed.sh` and `biom_export_needed.sh` export selected QIIME 2 results.
- `run_gtdb_pipeline.sh`, `run_silva_pipeline.sh`, and
	`run_gtdb_classification_pretrained.sh` run taxonomy-related steps.

## Typical use

1. Generate or copy the required input files into the pipeline-run directory.
2. Review the parameters and workflow commands in `snakemake_qiime.sh`.
3. Run quality control and inspect the FastQC or MultiQC results.
4. Run the Snakemake workflow with the selected QIIME 2 parameters.
5. Export and inspect results before uploading them to the database.

The scripts assume an HPC installation with QIIME 2 and Snakemake environments. Update the
environment paths and project-specific parameters when using this example for a new run.
