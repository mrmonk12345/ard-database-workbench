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
parser = argparse.ArgumentParser(description="Run pipeline")

parser.add_argument("--dataset-id", type=int, required=True, help="Dataset ID")

args = parser.parse_args()

dataset_id = args.dataset_id


print(f"dataset_id: {dataset_id}")




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


pipeline_run_id = create_pipeline_run(
    DATABASE_PATH,
    dataset_id
)

# --- paths ---
pipeline_dir = Path(PIPELINE_RUNS_PATH) / str(pipeline_run_id)
symlink_pipeline_dir = Path(ANALYSIS_DATASETS_PATH) / str(dataset_id) / "pipeline_runs" / str(pipeline_run_id)
example_pipeline_dir = Path(PIPELINE_RUNS_PATH) / "example_pipeline"


# --- create pipeline run directory ---
pipeline_dir.mkdir(parents=True, exist_ok=True)
symlink_pipeline_dir.parent.mkdir(parents=True, exist_ok=True)


# create symlink 

if not symlink_pipeline_dir.exists():
    symlink_pipeline_dir.symlink_to(
        pipeline_dir.resolve(),
        target_is_directory=True,
    )
    

# --- copy template pipeline ---
subprocess.run(
    ["rsync", "-av", f"{example_pipeline_dir}/", str(pipeline_dir)],
    check=True,
)


# Step 6
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