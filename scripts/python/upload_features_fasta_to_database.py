"""Load feature sequences from a FASTA file into the database."""

import sqlite3
from Bio import SeqIO


def load_features(
    fasta_file,
    db_path,
    pipeline_run_id,
    feature_type,
):
    """
    Insert feature records from a FASTA file.

    Each FASTA record is stored with the pipeline run ID, its sequence,
    and the FASTA record ID as the sequence hash.

    Args:
        fasta_file: Path to the FASTA file containing feature sequences.
        db_path: Path to the SQLite database.
        pipeline_run_id: ID of the associated pipeline run.
        feature_type: Type of the feature (asv or otu).
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    rows = []

    # Read each FASTA record and prepare its database values.
    for record in SeqIO.parse(fasta_file, "fasta"):
        rows.append(
            (
                pipeline_run_id,
                str(record.seq),
                record.id,
                feature_type,
            )
        )

    # Insert all parsed features in a single batch.
    cur.executemany(
        """
        INSERT INTO features (
            pipeline_run_id,
            sequence,
            sequence_hash,
            feature_type
        )
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )

    # Mark features as uploaded for this pipeline run.
    cur.execute(
    """
    UPDATE pipeline_runs
    SET features_uploaded = 1
    WHERE pipeline_run_id = ?
    """,
    (pipeline_run_id,),
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(rows):,} features")

if __name__ == "__main__":
    # Parse command-line arguments when the script is run directly.
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-run-id",
        required=True,
        type=int,
    )

    parser.add_argument(
        "--db-path",
        required=True,
    )

    parser.add_argument(
        "--fasta",
        required=True,
    )

    parser.add_argument(
        "--feature-type",
        default="asv",
    )

    args = parser.parse_args()

    # Load the FASTA records into the database.
    load_features(
        fasta_file=args.fasta,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
        feature_type=args.feature_type,
    )