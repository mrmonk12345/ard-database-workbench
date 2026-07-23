"""Update pipeline-run parameters from a Snakemake shell configuration."""

import argparse
import re
import sqlite3
from pathlib import Path

from config import ANALYSIS_DATASETS_PATH
from config import DATABASE_PATH
from config import PIPELINE_RUNS_PATH

# Parse the pipeline-run ID and optional database path from the command line.
parser = argparse.ArgumentParser(
    description="Update pipeline_runs from snakemake_qiime.sh"
)

parser.add_argument(
    "--pipeline-run-id",
    type=int,
    required=True,
    help="pipeline_runs.pipeline_run_id"
)



parser.add_argument(
    "--db",
    required=False,
    default=DATABASE_PATH,
    help="SQLite database path"
)

args = parser.parse_args()


def parse_shell_variables(path):
    """Read simple uppercase variable assignments from a shell file.

    Comments, empty lines, and lines that do not match ``KEY=VALUE`` are
    ignored. Matching values may optionally be enclosed in single or double
    quotes.
    """
    variables = {}

    # Match uppercase variable names containing letters and underscores.
    pattern = re.compile(r"^([A-Z_]+)=(.*)$")

    with open(path) as f:
        for line in f:
            line = line.strip()

            # Ignore blank lines and shell comments.
            if not line:
                continue

            if line.startswith("#"):
                continue

            match = pattern.match(line)

            if not match:
                continue

            key, value = match.groups()

            value = value.strip()

            # Remove matching surrounding quotes from the value.
            if (
                (value.startswith('"') and value.endswith('"'))
                or
                (value.startswith("'") and value.endswith("'"))
            ):
                value = value[1:-1]

            variables[key] = value

    return variables


conn = sqlite3.connect(args.db)
cur = conn.cursor()

# Retrieve the dataset associated with the selected pipeline run.
cur.execute(
    """
    SELECT analysis_dataset_id
    FROM pipeline_runs
    WHERE pipeline_run_id = ?
    """,
    (args.pipeline_run_id,)
)

row = cur.fetchone()

if row is None:
    raise RuntimeError(
        f"pipeline_run {args.pipeline_run_id} not found"
    )

dataset_id = row[0]

# Locate the Snakemake configuration file for this pipeline run.
config_path = (
    Path(PIPELINE_RUNS_PATH)
    / str(args.pipeline_run_id)
    / "snakemake_qiime.sh"
)

if not config_path.exists():
    raise FileNotFoundError(
        f"Config file not found: {config_path}"
    )

# Read parameter values from the shell configuration.
variables = parse_shell_variables(config_path)

# Update the pipeline-run record with the parsed QIIME parameters.
cur.execute(
    """
    UPDATE pipeline_runs
    SET
        trunc_len_f = ?,
        trunc_len_r = ?,
        p_max_ee_f = ?,
        p_max_ee_r = ?,
        p_min_overlap = ?,
        sampling_depth = ?,
        max_depth = ?
    WHERE pipeline_run_id = ?
    """,
    (
        variables.get("TRUNC_LEN_F"),
        variables.get("TRUNC_LEN_R"),
        variables.get("P_MAX_EE_F"),
        variables.get("P_MAX_EE_R"),
        variables.get("P_MIN_OVERLAP"),
        variables.get("SAMPLING_DEPTH"),
        variables.get("MAX_DEPTH"),
        args.pipeline_run_id,
    ),
)

if cur.rowcount == 0:
    raise RuntimeError(
        f"Failed updating pipeline_run {args.pipeline_run_id}"
    )

conn.commit()
conn.close()

print(
    f"Updated pipeline_run {args.pipeline_run_id} "
    f"from {config_path}"
)
