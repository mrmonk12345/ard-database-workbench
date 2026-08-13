"""Create all input files and a pipeline run directory for a dataset."""

import subprocess
from pathlib import Path
import argparse

from config import (
    DATABASE_PATH,
    RAW_READS_PATH,
    ANALYSIS_FILES_PATH,
    ANALYSIS_DATASETS_PATH,
    PIPELINE_RUNS_PATH,
    PYTHON_SCRIPTS_PATH,
)

from scripts.python.create_pipeline_run import create_pipeline_run

# --- parameters ---

# --- CLI arguments ---
# Parse the dataset selected for processing.
parser = argparse.ArgumentParser(description="Run pipeline")

parser.add_argument("--dataset-id", type=int, required=True, help="Dataset ID")

parser.add_argument(
    "--pipeline-run-id",
    type=int,
    help="Existing pipeline run ID to reuse; if omitted, a new pipeline run is created",
)

parser.add_argument(
    "--no-gzip",
    action="store_true",
    help="Skip raw read extraction and gzipping (Step 1)",
)


args = parser.parse_args()

dataset_id = args.dataset_id


print(f"dataset_id: {dataset_id}")




# --- helper to run steps ---
def run_step(script, args):
    cmd = ["python", str(Path(PYTHON_SCRIPTS_PATH) / script)] + args
    print("Running:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


# --- run pipeline steps ---

# Create gzipped FASTQ files from the raw reads.
if not args.no_gzip:
    run_step(
        "1_dataset_to_analysis_files_simple_gzip_multi_threaded.py",
        [
            "--dataset-id", str(dataset_id),
            "--db", str(DATABASE_PATH),
            "--fastq-dir", str(RAW_READS_PATH),
            "--outdir", str(ANALYSIS_FILES_PATH),
        ],
    )
else:
    print("Skipping FASTQ gzip step.")

# Create the QIIME FASTQ manifest.
run_step(
    "2_dataset_to_manifest_file.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--fastq-dir", str(ANALYSIS_FILES_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Create sample metadata for the dataset.
run_step(
    "3_dataset_to_sample_metadata.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Create amplicon metadata for the dataset.
run_step(
    "4_dataset_to_amplicon_metadata.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Create symlinks to the processed FASTQ files.
run_step(
    "5_dataset_symlink_files.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--files-dir", str(ANALYSIS_FILES_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Use existing pipeline run ID if provided, otherwise create one.
if args.pipeline_run_id is not None:
    pipeline_run_id = args.pipeline_run_id
    print(f"Using existing pipeline_run_id: {pipeline_run_id}")
else:
    pipeline_run_id = create_pipeline_run(
        DATABASE_PATH,
        dataset_id,
    )
    print(f"Created pipeline_run_id: {pipeline_run_id}")

# --- paths ---
# Define the pipeline run and dataset symlink locations.
pipeline_dir = Path(PIPELINE_RUNS_PATH) / str(pipeline_run_id)
symlink_pipeline_dir = Path(ANALYSIS_DATASETS_PATH) / str(dataset_id) / "pipeline_runs" / str(pipeline_run_id)
example_pipeline_dir = Path(PIPELINE_RUNS_PATH) / "example_pipeline"


# Create the pipeline run directory and its parent symlink directory.
pipeline_dir.mkdir(parents=True, exist_ok=True)
symlink_pipeline_dir.parent.mkdir(parents=True, exist_ok=True)


# Link the dataset to the corresponding pipeline run directory.
if not symlink_pipeline_dir.exists():
    symlink_pipeline_dir.symlink_to(
        pipeline_dir.resolve(),
        target_is_directory=True,
    )
    

# Copy the example pipeline structure into the new run directory.
subprocess.run(
    ["rsync", "-av", f"{example_pipeline_dir}/", str(pipeline_dir)],
    check=True,
)


# Copy the dataset metadata and FASTQ links into the pipeline run directory.
run_step(
    "6_dataset_directory_to_pipeline_run_directory.py",
    [
        "--dataset-id", str(dataset_id),
        "--pipeline-name", str(pipeline_run_id),
        "--dataset-dir-base", str(ANALYSIS_DATASETS_PATH),
        "--pipeline-dir-base", str(PIPELINE_RUNS_PATH),
    ],
)


print("? Pipeline completed")