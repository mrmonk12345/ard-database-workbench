import sqlite3
import pandas as pd


def load_feature_counts(
    tsv_file,
    db_path,
    pipeline_run_id,
):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Skip metadata line and read whitespace-delimited table
    df = pd.read_csv(
        tsv_file,
        sep="\t",
        skiprows=1,
        engine="python",
    )

    # Rename first column to sequence_hash
    df.rename(
        columns={df.columns[0]: "sequence_hash"},
        inplace=True,
    )

    # ASV lookup
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

    # Analysis unit lookup
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

    for _, row in df.iterrows():

        asv_id = asv_lookup.get(row["sequence_hash"])

        if asv_id is None:
            continue

        for sample_name in df.columns[1:]:

            count = float(row[sample_name])

            if count == 0:
                continue

            analysis_unit_id = au_lookup.get(sample_name)

            # If DB stores only AU229 instead of sample326_AU229
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

    load_feature_counts(
        tsv_file=args.table,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
    )