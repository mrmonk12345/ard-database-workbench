"""Assign base analysis units to an analysis dataset."""

import sqlite3
import pandas as pd
import argparse

from scripts.python.dataset_base_make_inputs import create_dataset_inputs
from config import DATABASE_PATH

# Find analysis units that are already assigned to the dataset.
SELECT_EXISTING_INPUTS_SQL = """
SELECT analysis_unit_id
FROM analysis_units
WHERE analysis_dataset_id = ?
"""

# Assign an analysis unit to the selected dataset.
UPDATE_INPUT_SQL = """
UPDATE analysis_units
SET analysis_dataset_id = ?
WHERE analysis_unit_id = ?
"""


def sync_dataset_inputs(dataset_id, db_path=DATABASE_PATH, no_commit=False):
    """Assign missing base analysis units to a dataset.

    If the dataset has no inputs, all expected analysis units are assigned.
    If the dataset already has inputs, the function only reports whether any
    expected units are missing and does not modify the existing assignments.

    Args:
        dataset_id: ID of the analysis dataset to update.
        db_path: Path to the SQLite database.
        no_commit: If True, show planned changes without saving them.
    """

    # Determine which analysis units are expected for this dataset.
    expected_df = create_dataset_inputs(
        db_path=db_path,
        dataset_id=dataset_id
    )

    expected_au_ids = set(expected_df["analysis_unit_id"])

    conn = sqlite3.connect(db_path)

    try:
        # Load analysis units currently assigned to the dataset.
        existing_df = pd.read_sql_query(
            SELECT_EXISTING_INPUTS_SQL,
            conn,
            params=(dataset_id,)
        )

        existing_au_ids = set(existing_df["analysis_unit_id"])

        # Initialize a dataset that does not have any inputs yet.
        if len(existing_au_ids) == 0:
            rows_to_insert = [
                (dataset_id, au_id)
                for au_id in expected_au_ids
            ]
        
            if no_commit:
                print(
                    f"DRY RUN: Dataset {dataset_id} had no inputs. "
                    f"Would insert {len(rows_to_insert)} base inputs."
                )
            else:
                conn.executemany(
                    UPDATE_INPUT_SQL,
                    rows_to_insert
                )
                conn.commit()
        
                print(
                    f"Dataset {dataset_id} had no inputs. "
                    f"Inserted {len(rows_to_insert)} base inputs."
                )
        
            return

        # Do not modify a dataset that already contains inputs.
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
    # Parse command-line options when the script is run directly.
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
    
    parser.add_argument(
    "--no-commit",
    action="store_true",
    help="Dry run only. Do not commit any database changes."
    )

    args = parser.parse_args()

    # Synchronize the selected dataset with its expected analysis units.
    sync_dataset_inputs(
        dataset_id=args.dataset_id,
        db_path=args.db,
        no_commit = args.no_commit
    )
