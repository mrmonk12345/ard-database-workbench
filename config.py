from pathlib import Path
import yaml


# --- config.yml path ---
CONFIG_PATH = Path.cwd() / "config.yml"

# --- Optional override ---
# CONFIG_PATH = Path("/absolute/path/to/config.yml")


if not CONFIG_PATH.exists():
    raise RuntimeError(f"config.yml file not found: {CONFIG_PATH}")


# --- load YAML ---
with open(CONFIG_PATH, "r") as f:
    _config = yaml.safe_load(f)


# --- helper ---
def get_config(path: str):
    keys = path.split(".")
    value = _config

    for key in keys:
        if key not in value:
            raise RuntimeError(f"Missing config key: {path}")
        value = value[key]

    return value


# --- paths ---
WORKING_DIRECTORY_PATH = get_config("paths.working_directory")
DATABASE_PATH = get_config("paths.database")
RAW_READS_PATH = get_config("paths.raw_reads")
ANALYSIS_FILES_PATH = get_config("paths.analysis_files")
ANALYSIS_DATASETS_PATH = get_config("paths.analysis_datasets")
PIPELINE_RUNS_PATH = get_config("paths.pipeline_runs")
PYTHON_SCRIPTS_PATH = get_config("paths.python_scripts")
