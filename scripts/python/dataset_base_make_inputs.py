import sqlite3
import pandas as pd

from config import DATABASE_PATH

# --- SQL QUERIES ---

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
    conn = sqlite3.connect(db_path)

    # Load into pandas DataFrame directly
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