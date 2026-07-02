import sqlite3
import pandas as pd
import argparse

from scripts.python.dataset_base_make_inputs import create_dataset_inputs
from config import DATABASE_PATH


SELECT_EXISTING_INPUTS_SQL = """
SELECT analysis_unit_id
FROM analysis_dataset_inputs
WHERE analysis_dataset_id = ?
"""

INSERT_INPUT_SQL = """
INSERT INTO analysis_dataset_inputs (
    analysis_dataset_id,
    analysis_unit_id
)
VALUES (?, ?)
"""


def sync_dataset_inputs(dataset_id, db_path=DATABASE_PATH):
    """
    Inserts base inputs only if the dataset currently has no inputs.

    If inputs already exist:
      - Prints OK if all base inputs exist.
      - Prints a warning if some base inputs are missing.
      - Does NOT modify the dataset.
    """

    expected_df = create_dataset_inputs(
        db_path=db_path,
        dataset_id=dataset_id
    )

    expected_au_ids = set(expected_df["analysis_unit_id"])

    conn = sqlite3.connect(db_path)

    try:
        existing_df = pd.read_sql_query(
            SELECT_EXISTING_INPUTS_SQL,
            conn,
            params=(dataset_id,)
        )

        existing_au_ids = set(existing_df["analysis_unit_id"])

        # Dataset has no inputs -> initialize it
        if len(existing_au_ids) == 0:
            rows_to_insert = [
                (dataset_id, au_id)
                for au_id in expected_au_ids
            ]

            conn.executemany(
                INSERT_INPUT_SQL,
                rows_to_insert
            )

            conn.commit()

            print(
                f"Dataset {dataset_id} had no inputs. "
                f"Inserted {len(rows_to_insert)} base inputs."
            )
            return

        # Dataset already has inputs
        missing_au_ids = expected_au_ids - existing_au_ids

        if not missing_au_ids:
            print(
                f"Dataset {dataset_id} already contains "
                f"all {len(expected_au_ids)} base inputs."
            )
        else:
            print(
                f"WARNING: Dataset {dataset_id} already has inputs "
                f"but is missing {len(missing_au_ids)} base inputs. "
                f"No changes were made."
            )
            print(
                f"Missing analysis_unit_ids: "
                f"{sorted(missing_au_ids)}"
            )

    finally:
        conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialize analysis_dataset_inputs for a dataset."
    )

    parser.add_argument(
        "--dataset-id",
        required=True,
        type=int,
        help="Analysis dataset ID"
    )

    parser.add_argument(
        "--db",
        default=DATABASE_PATH,
        help="Path to SQLite database"
    )

    args = parser.parse_args()

    sync_dataset_inputs(
        dataset_id=args.dataset_id,
        db_path=args.db
    )
