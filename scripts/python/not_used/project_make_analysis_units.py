"""
input:
library,
sequencing_runs

output:
analysis_units
"""

import sqlite3

DB_PATH = "project.db"


def make_analysis_units(library_runs):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for item in library_runs:
        library_id = item["library_id"]

        for run_id in item["sequencing_run_ids"]:

            # ✅ check if already exists
            cur.execute("""
                SELECT 1 FROM analysis_units
                WHERE library_id = ? AND sequencing_run_id = ?
            """, (library_id, run_id))

            if cur.fetchone():
                print(f"[EXISTS] library {library_id} + run {run_id}")
                continue

            # ✅ insert
            cur.execute("""
                INSERT INTO analysis_units (
                    library_id,
                    sequencing_run_id
                )
                VALUES (?, ?)
            """, (library_id, run_id))

            print(f"[ADD] library {library_id} + run {run_id}")

    conn.commit()
    conn.close()