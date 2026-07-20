import subprocess
from pathlib import Path
import argparse

from config import (
    PIPELINE_RUNS_PATH,
    PYTHON_SCRIPTS_PATH,
    DATABASE_PATH,
)


def load_pipeline_run(pipeline_run_id: int):

    export_dir = (
        Path(PIPELINE_RUNS_PATH)
        / str(pipeline_run_id)
        / "exported"
    )

    scripts_dir = Path(PYTHON_SCRIPTS_PATH)

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

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-run-id",
        required=True,
        type=int,
    )

    args = parser.parse_args()

    load_pipeline_run(args.pipeline_run_id)