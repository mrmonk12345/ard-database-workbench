import sqlite3
import pandas as pd

from config import DATABASE_PATH


def run_query(query, params=None):
    conn = sqlite3.connect(DATABASE_PATH)

    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df


def get_project_ids():
    query = """
    SELECT project_id
    FROM projects
    """
    return run_query(query)     

def get_amplicon_types():
    query = """
    SELECT *
    FROM amplicon_types
    """
    return run_query(query)

def get_sequencing_runs():
    query = """
    SELECT *
    FROM sequencing_runs
    """
    return run_query(query)