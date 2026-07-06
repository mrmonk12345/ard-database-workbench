import sqlite3

from config import DATABASE_PATH


def update_null_au_names():
    sql = """
    UPDATE analysis_units
    SET analysis_unit_name = (
        SELECT 'sample' || l.sample_id || '_AU' || analysis_units.analysis_unit_id
        FROM libraries l
        WHERE l.library_id = analysis_units.library_id
    )
    WHERE (analysis_unit_name IS NULL OR analysis_unit_name = '');
    """

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.executescript(sql)
        conn.commit()
        print("Analysis unit names updated successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    update_null_au_names()