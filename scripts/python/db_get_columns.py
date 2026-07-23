"""Retrieve column names from a SQLite database table."""

import sqlite3

from config import DATABASE_PATH


def get_table_columns(table_name):
    """Return the column names for a database table.

    Args:
        table_name: Name of the table to inspect.

    Returns:
        A list containing the table's column names.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table_name})")

    columns = [row[1] for row in cur.fetchall()]

    conn.close()
    return columns