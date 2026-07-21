import sqlite3
from pathlib import Path


def create_pipeline_run(db_path, dataset_id, pipeline_definition_id=1):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pipeline_runs (
            analysis_dataset_id,
            pipeline_definition_id
        )
        VALUES (?, ?)
        """,
        (dataset_id, pipeline_definition_id)
    )

    pipeline_run_id = cur.lastrowid


    conn.commit()
    conn.close()

    return pipeline_run_id