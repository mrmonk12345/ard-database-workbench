# Classifiers

This directory contains shell scripts for downloading or preparing QIIME 2 taxonomy reference
data. The resulting `.qza` files are reference inputs for taxonomy classification pipelines.

## Scripts

- `rescript_silva.sh` downloads SILVA taxonomy and sequences, then reverse-transcribes the
  sequences for use with DNA data.
- `rescript_gtdb.sh` downloads GTDB taxonomy and sequence data for the configured version.

Review the database version, target, and output filenames in each script before running it.
The scripts load the QIIME 2 environment from the HPC installation, so they must be run where
that environment is available. Keep large classifier files outside Git unless they are
specifically intended to be versioned.