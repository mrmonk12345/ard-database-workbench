
"""Load analysis unit IDs associated with an analysis dataset."""

import sqlite3
import pandas as pd

from config import DATABASE_PATH


# Select analysis units that match the dataset's sequencing run and amplicon type.
SELECT_AU_IDS_FOR_DATASET_SQL = """
SELECT au.analysis_unit_id
FROM analysis_datasets ad
JOIN analysis_units au
    ON ad.sequencing_run_id = au.sequencing_run_id
JOIN libraries l
    ON au.library_id = l.library_id
WHERE 
    ad.analysis_dataset_id = ?
    AND ad.sequencing_run_id = au.sequencing_run_id
    AND ad.amplicon_type_id = l.amplicon_type_id;
"""


# --- FUNCTION ---

def create_dataset_inputs(db_path=DATABASE_PATH, dataset_id=None):
    """Return analysis unit IDs for the selected dataset as a DataFrame.

    Args:
        db_path: Path to the SQLite database.
        dataset_id: ID of the analysis dataset to query.

    Returns:
        A pandas DataFrame containing the matching analysis unit IDs.
    """
    conn = sqlite3.connect(db_path)

    # Execute the query and load the results directly into pandas.
    df = pd.read_sql_query(
        SELECT_AU_IDS_FOR_DATASET_SQL,
        conn,
        params=(dataset_id,)
    )

    conn.close()

    print(f"Fetched {len(df)} rows.")

    return df


# Example usage
#df = create_dataset_inputs("your_database.db", 1)
#print(df.head())