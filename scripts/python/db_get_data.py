import sqlite3
import pandas as pd

from config import DATABASE_PATH


def get_projects():
    conn = sqlite3.connect(DATABASE_PATH)

    query = """
    SELECT project_id
    FROM projects
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df