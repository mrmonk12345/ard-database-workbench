"""Provide helper functions for reading database data into pandas DataFrames."""

import sqlite3
import pandas as pd

from config import DATABASE_PATH


def run_query(query, params=None):
    """Execute a SQL query and return the results as a DataFrame.

    Args:
        query: SQL query to execute.
        params: Optional parameters used by the query placeholders.

    Returns:
        A pandas DataFrame containing the query results.
    """
    conn = sqlite3.connect(DATABASE_PATH)

    # Use parameterized queries when parameters are provided.
    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df


def get_project_ids():
    """Return the IDs of all projects."""
    query = """
    SELECT project_id
    FROM projects
    """
    return run_query(query)     

def get_projects():
    """Return all project records."""
    query = """
    SELECT *
    FROM projects
    """
    return run_query(query)     

def get_amplicon_types():
    """Return all amplicon type records."""
    query = """
    SELECT *
    FROM amplicon_types
    """
    return run_query(query)

def get_sequencing_runs():
    """Return all sequencing run records."""
    query = """
    SELECT *
    FROM sequencing_runs
    """
    return run_query(query)
    
def get_treatments():
    """Return all treatment records."""
    query = """
    SELECT *
    FROM treatments
    """
    return run_query(query)