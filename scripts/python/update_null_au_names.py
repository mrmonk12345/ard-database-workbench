import sqlite3
import argparse

from config import DATABASE_PATH


def update_null_au_names(project_id):
    """
    Assign names to analysis units without a name for a specific project.

    Names are generated as:
        sample<SAMPLE_ID>_AU<ANALYSIS_UNIT_ID>
    """

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = conn.cursor()

        rows = cursor.execute(
            """
            SELECT
                au.analysis_unit_id,
                l.sample_id,
                'sample' || l.sample_id || '_AU' || au.analysis_unit_id AS new_name
            FROM analysis_units au
            JOIN libraries l
                ON au.library_id = l.library_id
            JOIN samples s
                ON l.sample_id = s.sample_id
            WHERE (au.analysis_unit_name IS NULL OR au.analysis_unit_name = '')
              AND s.project_id = ?
            """,
            (project_id,),
        ).fetchall()

        if not rows:
            print(f"No null analysis units found for project_id={project_id}")
            return

        print("Will update:")
        for analysis_unit_id, sample_id, new_name in rows:
            print(
                f"  analysis_unit_id={analysis_unit_id}, "
                f"sample_id={sample_id} -> {new_name}"
            )

        cursor.execute(
            """
            UPDATE analysis_units
            SET analysis_unit_name = (
                SELECT
                    'sample' || l.sample_id || '_AU' || analysis_units.analysis_unit_id
                FROM libraries l
                WHERE l.library_id = analysis_units.library_id
            )
            WHERE (analysis_unit_name IS NULL OR analysis_unit_name = '')
            AND library_id IN (
                SELECT l.library_id
                FROM libraries l
                JOIN samples s
                    ON l.sample_id = s.sample_id
                WHERE s.project_id = ?
            )
            """,
            (project_id,),
        )

        conn.commit()

        updated = cursor.rowcount
        skipped = len(rows) - updated

        print(f"\nUpdated {updated} analysis units.")
        print(f"Skipped {skipped} analysis units.")

    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fill missing analysis unit names for a project."
    )

    parser.add_argument(
        "-p",
        "--project-id",
        type=int,
        required=True,
        help="Project ID",
    )

    args = parser.parse_args()

    update_null_au_names(args.project_id)