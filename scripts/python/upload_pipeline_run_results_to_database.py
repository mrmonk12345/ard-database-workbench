"""Load exported pipeline results into the database."""

import subprocess
from pathlib import Path
import argparse

from config import (
    PIPELINE_RUNS_PATH,
    PYTHON_SCRIPTS_PATH,
    DATABASE_PATH,
)


def load_pipeline_run(pipeline_run_id: int):
    """
    Load ASVs, feature counts, and taxonomy for a pipeline run.

    The expected exported files are located in the pipeline run's
    ``exported`` directory. Each result type is loaded by its corresponding
    helper script.

    Args:
        pipeline_run_id: ID of the pipeline run to load.
    """
    # Locate the exported results and helper scripts.
    export_dir = (
        Path(PIPELINE_RUNS_PATH)
        / str(pipeline_run_id)
        / "exported"
    )

    scripts_dir = Path(PYTHON_SCRIPTS_PATH)

    # Load ASV sequences from the exported FASTA file.
    subprocess.run(
        [
            "python",
            str(scripts_dir / "upload_asvs_fasta_to_database.py"),
            "--pipeline-run-id",
            str(pipeline_run_id),
            "--db-path",
            DATABASE_PATH,
            "--fasta",
            str(export_dir / "dna-sequences.fasta"),
        ],
        check=True,
    )

    # Load non-zero ASV feature counts from the exported feature table.
    subprocess.run(
        [
            "python",
            str(scripts_dir / "upload_feature_counts_to_database.py"),
            "--pipeline-run-id",
            str(pipeline_run_id),
            "--db-path",
            DATABASE_PATH,
            "--table",
            str(export_dir / "feature-table.tsv"),
        ],
        check=True,
    )

    # Load ASV taxonomy assignments from the exported taxonomy file.
    subprocess.run(
        [
            "python",
            str(scripts_dir / "upload_taxonomy_to_database.py"),
            "--pipeline-run-id",
            str(pipeline_run_id),
            "--db-path",
            DATABASE_PATH,
            "--taxonomy",
            str(export_dir / "taxonomy.tsv"),
        ],
        check=True,
    )

    print(f"Finished loading pipeline run {pipeline_run_id}")


if __name__ == "__main__":
    # Parse the pipeline-run ID when the script is run directly.
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-run-id",
        required=True,
        type=int,
    )

    args = parser.parse_args()

    # Load all exported results for the selected pipeline run.
    load_pipeline_run(args.pipeline_run_id)