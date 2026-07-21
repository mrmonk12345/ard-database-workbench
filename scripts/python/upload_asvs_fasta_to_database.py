import sqlite3
from Bio import SeqIO


def load_asvs(
    fasta_file,
    db_path,
    pipeline_run_id,
):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    rows = []

    for record in SeqIO.parse(fasta_file, "fasta"):
        rows.append(
            (
                pipeline_run_id,
                str(record.seq),
                record.id,
            )
        )

    cur.executemany(
        """
        INSERT INTO asvs (
            pipeline_run_id,
            sequence,
            sequence_hash
        )
        VALUES (?, ?, ?)
        """,
        rows,
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(rows):,} ASVs")

if __name__ == "__main__":

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

    args = parser.parse_args()

    load_asvs(
        fasta_file=args.fasta,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
    )