import sqlite3

DB_PATH = "project.db"


def create_base_datasets(project_id=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # -----------------------------------
    # 1. Find valid dataset combinations
    # -----------------------------------
    cur.execute("""
        SELECT 
            au.sequencing_run_id,
            l.amplicon_type_id,
            COUNT(*) as unit_count
        FROM analysis_units au
        JOIN libraries l ON au.library_id = l.library_id
        JOIN sequencing_runs sr ON au.sequencing_run_id = sr.sequencing_run_id
        WHERE (? IS NULL OR sr.project_id = ?)
        GROUP BY au.sequencing_run_id, l.amplicon_type_id
        HAVING COUNT(*) > 0
    """, (project_id, project_id))

    combos = cur.fetchall()

    print(f"[INFO] Found {len(combos)} valid dataset groups")

    # -----------------------------------
    # 2. Create datasets + insert units
    # -----------------------------------
    for sequencing_run_id, amplicon_type_id, unit_count in combos:

        # check if dataset exists
        cur.execute("""
            SELECT analysis_dataset_id
            FROM analysis_datasets
            WHERE sequencing_run_id = ?
              AND amplicon_type_id = ?
        """, (sequencing_run_id, amplicon_type_id))

        row = cur.fetchone()

        if row:
            dataset_id = row[0]
            print(f"[ALREADY EXISTS] run={sequencing_run_id}, amp={amplicon_type_id}")
        else:
            cur.execute("""
                INSERT INTO analysis_datasets (
                    sequencing_run_id,
                    amplicon_type_id
                )
                VALUES (?, ?)
            """, (sequencing_run_id, amplicon_type_id))

            dataset_id = cur.lastrowid
            print(f"[DATASET CREATED] run={sequencing_run_id}, amp={amplicon_type_id}")

        # -----------------------------------
        # 3. Insert analysis units
        # -----------------------------------
        cur.execute("""
            INSERT INTO analysis_dataset_inputs (
                analysis_dataset_id,
                analysis_unit_id
            )
            SELECT ?, au.analysis_unit_id
            FROM analysis_units au
            JOIN libraries l ON au.library_id = l.library_id
            WHERE au.sequencing_run_id = ?
              AND l.amplicon_type_id = ?
              AND NOT EXISTS (
                  SELECT 1
                  FROM analysis_dataset_inputs adi
                  WHERE adi.analysis_dataset_id = ?
                    AND adi.analysis_unit_id = au.analysis_unit_id
              )
        """, (
            dataset_id,
            sequencing_run_id,
            amplicon_type_id,
            dataset_id
        ))

        print(f"[LINKED] dataset {dataset_id} ← units added")

    conn.commit()
    conn.close()
