from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except ImportError:
    raise RuntimeError("python-dotenv is required but not installed")


# --- .env path ---
# Default: use .env from current working directory
ENV_PATH = Path.cwd() / ".env"

# --- Optional override (uncomment if needed) ---
# ENV_PATH = Path("/home/ARO.local/michaelr/Projects/db_collab_github/ARD_DB_tools/.env")


if not ENV_PATH.exists():
    raise RuntimeError(f".env file not found: {ENV_PATH}")


# --- load .env ---
load_dotenv(ENV_PATH)


# --- helper ---
def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


# --- paths ---
WORKING_DIRECTORY = get_env("WORKING_DIRECTORY_PATH")
DATABASE_PATH = get_env("DATABASE_PATH")
RAW_READS_PATH = get_env("RAW_READS_PATH")
ANALYSIS_FILES_PATH = get_env("ANALYSIS_FILES_PATH")
ANALYSIS_DATASETS_PATH = get_env("ANALYSIS_DATASETS_PATH")
PIPELINE_RUNS_PATH = get_env("PIPELINE_RUNS_PATH")