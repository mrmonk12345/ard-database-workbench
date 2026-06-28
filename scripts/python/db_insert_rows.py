import sqlite3

from config import DATABASE_PATH


def insert_rows(table_name, rows):
    if not rows:
        print("No rows to insert")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    # Extract columns from first row
    columns = list(rows[0].keys())

    # Build query
    col_str = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))

    query = f"""
        INSERT INTO {table_name} ({col_str})
        VALUES ({placeholders})
    """

    for row in rows:
        values = tuple(row.get(col) for col in columns)

        cur.execute(query, values)

        print(f"[ADD] {row}")

    conn.commit()
    conn.close()