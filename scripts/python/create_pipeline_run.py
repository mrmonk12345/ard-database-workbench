"""Create a pipeline run record for an analysis dataset."""

import sqlite3
from pathlib import Path


def create_pipeline_run(db_path, dataset_id, pipeline_definition_id=1):
    """Insert a pipeline run and return its generated ID.

    Args:
        db_path: Path to the SQLite database.
        dataset_id: ID of the analysis dataset.
        pipeline_definition_id: ID of the pipeline definition to use.

    Returns:
        The ID assigned to the new pipeline run.
    """
    # Open the database and prepare a cursor for the insert.
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create a pipeline run linked to the selected dataset and definition.
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

    # SQLite provides the generated ID for the newly inserted record.
    pipeline_run_id = cur.lastrowid

    # Save the new record and close the database connection.
    conn.commit()
    conn.close()

    return pipeline_run_id