"""
input:
sample,
amplicon_types

output:
libraries
"""

import sqlite3

DB_PATH = "project.db"


def make_libraries(sample_amplicons):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for item in sample_amplicons:
        sample_id = item["sample_id"]

        for amp_id in item["amplicon_type_ids"]:

            # ✅ check if already exists
            cur.execute("""
                SELECT 1 FROM libraries
                WHERE sample_id = ? AND amplicon_type_id = ?
            """, (sample_id, amp_id))

            if cur.fetchone():
                print(f"[EXISTS] sample {sample_id} + amplicon {amp_id}")
                continue

            # ✅ insert if not exists
            cur.execute("""
                INSERT INTO libraries (
                    sample_id,
                    amplicon_type_id
                )
                VALUES (?, ?)
            """, (sample_id, amp_id))

            print(f"[ADD] sample {sample_id} + amplicon {amp_id}")

    conn.commit()
    conn.close()