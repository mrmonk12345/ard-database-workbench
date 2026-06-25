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


# --- parameters ---

# --- CLI arguments ---
parser = argparse.ArgumentParser(description="Run pipeline")

parser.add_argument("--dataset-id", type=int, required=True, help="Dataset ID")
parser.add_argument("--pipeline-name", required=True, help="Pipeline name")

args = parser.parse_args()

dataset_id = args.dataset_id
pipeline_name = args.pipeline_name


print(f"dataset_id: {dataset_id}")
print(f"pipeline_name: {pipeline_name}")


# --- paths ---
pipeline_dir = Path(PIPELINE_RUNS_PATH) / pipeline_name
example_pipeline_dir = Path(PIPELINE_RUNS_PATH) / "example_pipeline"


# --- create pipeline run directory ---
pipeline_dir.mkdir(parents=True, exist_ok=True)


# --- copy template pipeline ---
subprocess.run(
    ["rsync", "-av", f"{example_pipeline_dir}/", str(pipeline_dir)],
    check=True,
)


# --- helper to run steps ---
def run_step(script, args):
    cmd = ["python", str(Path(PYTHON_SCRIPTS_PATH) / script)] + args
    print("Running:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


# --- run pipeline steps ---

# Step 1
run_step(
    "1_dataset_to_analysis_files_simple_gzip_multi_threaded.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--fastq-dir", str(RAW_READS_PATH),
        "--outdir", str(ANALYSIS_FILES_PATH),
    ],
)

# Step 2
run_step(
    "2_dataset_to_manifest_file.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--fastq-dir", str(ANALYSIS_FILES_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Step 3
run_step(
    "3_dataset_to_sample_metadata.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Step 4
run_step(
    "4_dataset_to_amplicon_metadata.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Step 5
run_step(
    "5_dataset_symlink_files.py",
    [
        "--dataset-id", str(dataset_id),
        "--db", str(DATABASE_PATH),
        "--files-dir", str(ANALYSIS_FILES_PATH),
        "--outdir-base", str(ANALYSIS_DATASETS_PATH),
    ],
)

# Step 6
run_step(
    "6_dataset_directory_to_pipeline_run_directory.py",
    [
        "--dataset-id", str(dataset_id),
        "--pipeline-name", pipeline_name,
        "--dataset-dir-base", str(ANALYSIS_DATASETS_PATH),
        "--pipeline-dir-base", str(PIPELINE_RUNS_PATH),
    ],
)


print("? Pipeline completed")