import sqlite3


def create_pipeline_run(db_path, dataset_id):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pipeline_runs (
            analysis_dataset_id
        )
        VALUES (?)
        """,
        (dataset_id,),
    )

    pipeline_run_id = cur.lastrowid

    conn.commit()
    conn.close()

    return pipeline_run_id