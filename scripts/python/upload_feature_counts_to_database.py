"""Load ASV feature counts from a TSV file into the database."""

import sqlite3
import pandas as pd


def load_feature_counts(
    tsv_file,
    db_path,
    pipeline_run_id,
):
    """
    Insert non-zero ASV feature counts for a pipeline run.

    The TSV file is expected to contain ASV sequence hashes in the first
    column and analysis-unit names in the remaining columns.

    Args:
        tsv_file: Path to the feature-count TSV file.
        db_path: Path to the SQLite database.
        pipeline_run_id: ID of the associated pipeline run.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Skip the metadata line and read the tab-separated feature table.
    df = pd.read_csv(
        tsv_file,
        sep="\t",
        skiprows=1,
        engine="python",
    )

    # The first column contains the sequence hash used to identify each ASV.
    df.rename(
        columns={df.columns[0]: "sequence_hash"},
        inplace=True,
    )

    # Build a lookup from sequence hashes to ASV IDs for this pipeline run.
    asv_lookup = dict(
        cur.execute(
            """
            SELECT sequence_hash, asv_id
            FROM asvs
            WHERE pipeline_run_id = ?
            """,
            (pipeline_run_id,),
        )
    )

    # Build a lookup from analysis-unit names to their database IDs.
    au_lookup = dict(
        cur.execute(
            """
            SELECT
                analysis_unit_name,
                analysis_unit_id
            FROM analysis_units
            """
        )
    )

    rows = []

    # Process each ASV and its counts across all analysis units.
    for _, row in df.iterrows():

        asv_id = asv_lookup.get(row["sequence_hash"])

        if asv_id is None:
            continue

        for sample_name in df.columns[1:]:

            count = float(row[sample_name])

            # Zero counts do not need to be stored.
            if count == 0:
                continue

            analysis_unit_id = au_lookup.get(sample_name)

            # Support names such as sample326_AU229 when the database
            # stores only the shorter AU229 analysis-unit name.
            if analysis_unit_id is None and "_" in sample_name:
                analysis_unit_id = au_lookup.get(
                    sample_name.split("_")[-1]
                )

            if analysis_unit_id is None:
                print(
                    f"Missing analysis unit: {sample_name}"
                )
                continue

            rows.append(
                (
                    asv_id,
                    analysis_unit_id,
                    pipeline_run_id,
                    int(count),
                )
            )

    # Insert all feature counts in one batch.
    cur.executemany(
        """
        INSERT INTO feature_counts (
            asv_id,
            analysis_unit_id,
            pipeline_run_id,
            count
        )
        VALUES (?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()
    conn.close()

    print(
        f"Inserted {len(rows):,} feature counts"
    )

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
        "--table",
        required=True,
    )

    args = parser.parse_args()

    # Load the feature counts into the database.
    load_feature_counts(
        tsv_file=args.table,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
    )