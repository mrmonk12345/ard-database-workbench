#!/bin/bash

# --- load environment variables ---
set -a
source /home/ARO.local/michaelr/Projects/db_collab_github/ARD_DB_tools/.env
set +a

echo "WORKING_DIRECTORY=$WORKING_DIRECTORY"


# --- parameters ---
dataset_id=2
pipeline_name="2"

echo "dataset_id: $dataset_id"
echo "pipeline_name: $pipeline_name"

# --- create pipeline run directory ---
mkdir -p "$PIPELINE_RUNS_PATH/$pipeline_name"

# --- copy template pipeline ---
rsync -av "$PIPELINE_RUNS_PATH/example_pipeline/" \
          "$PIPELINE_RUNS_PATH/$pipeline_name"

# --- run pipeline steps ---

# Step 1 (optional)
 python $PYTHON_SCRIPTS_PATH/1_dataset_to_analysis_files_simple_gzip_multi_threaded.py \
   --dataset-id $dataset_id \
   --db $DATABASE_PATH \
   --fastq-dir $RAW_READS_PATH \
   --outdir $ANALYSIS_FILES_PATH

# Step 2
python $PYTHON_SCRIPTS_PATH/2_dataset_to_manifest_file.py \
  --dataset-id $dataset_id \
  --db $DATABASE_PATH \
  --fastq-dir $ANALYSIS_FILES_PATH \
  --outdir-base $ANALYSIS_DATASETS_PATH

# Step 3
python $PYTHON_SCRIPTS_PATH/3_dataset_to_sample_metadata.py \
  --dataset-id $dataset_id \
  --db $DATABASE_PATH \
  --outdir-base $ANALYSIS_DATASETS_PATH

# Step 4
python $PYTHON_SCRIPTS_PATH/4_dataset_to_amplicon_metadata.py \
  --dataset-id $dataset_id \
  --db $DATABASE_PATH \
  --outdir-base $ANALYSIS_DATASETS_PATH

# Step 5
python $PYTHON_SCRIPTS_PATH/5_dataset_symlink_files.py \
  --dataset-id $dataset_id \
  --db $DATABASE_PATH \
  --files-dir $ANALYSIS_FILES_PATH \
  --outdir-base $ANALYSIS_DATASETS_PATH

# Step 6
python $PYTHON_SCRIPTS_PATH/6_dataset_directory_to_pipeline_run_directory.py \
  --dataset-id $dataset_id \
  --pipeline-name $pipeline_name \
  --dataset-dir-base $ANALYSIS_DATASETS_PATH \
  --pipeline-dir-base $PIPELINE_RUNS_PATH

echo "? Pipeline completed"