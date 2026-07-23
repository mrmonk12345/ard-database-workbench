"""Load tab-separated data into a SQLite database table."""

import sqlite3
import csv
import argparse

from config import DATABASE_PATH

def is_empty_row(row):
    """Return True when all fields in a row are empty."""
    return all(v is None or str(v).strip() == "" for v in row.values())

def get_connection(db_path):
    """Open and return a connection to the SQLite database."""
    return sqlite3.connect(db_path)


def build_query(table, columns, mode):
    """Build an INSERT query using the selected conflict-handling mode.

    Args:
        table: Destination database table.
        columns: Column names supplied by the TSV header.
        mode: Conflict behavior: skip, replace, or fail.

    Returns:
        A parameterized SQL INSERT statement.
    """
    placeholders = ", ".join(["?"] * len(columns))
    cols = ", ".join(columns)

    if mode == "replace":
        return f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})"
    elif mode == "skip":
        return f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({placeholders})"
    else:  # fail
        # Use a normal INSERT so constraint violations are reported.
        return f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"


def load_tsv(args):
    """
    Load rows from a TSV file into the selected database table.

    Empty rows are ignored. Empty field values are converted to SQL NULL.
    Changes are committed immediately unless dry-run mode is enabled.
    """
    conn = get_connection(args.db)
    cursor = conn.cursor()

    inserted = 0
    skipped = 0
    failed = 0

    # Read the TSV header to determine the destination columns.
    with open(args.file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        query = build_query(args.table, reader.fieldnames, args.mode)

        # TSV data starts on line 2 because line 1 contains the header.
        for line_num, row in enumerate(reader, start=2):          
            if is_empty_row(row):
                if args.verbose:
                    print(f"[SKIPPED EMPTY] line {line_num}")
                continue
            try:
                # Track changes to distinguish inserted rows from ignored rows.
                before_changes = conn.total_changes

                # Convert blank TSV values to SQL NULL.
                true_values = [
                    None if v is None or str(v).strip() == "" else v
                    for v in row.values()
                ]

                cursor.execute(query, true_values)

                if not args.no_commit:
                    conn.commit()

                if conn.total_changes == before_changes:
                    skipped += 1
                    if args.verbose:
                        print(f"[SKIPPED] line {line_num}: {row}")
                else:
                    inserted += 1
                    if args.verbose:
                        print(f"[INSERTED] line {line_num}")

            except sqlite3.IntegrityError as e:
                failed += 1
                print(f"[FAILED] line {line_num}: {e} -> {row}")

            except Exception as e:
                failed += 1
                print(f"[ERROR] line {line_num}: {e} -> {row}")

    # Commit any pending changes unless this is a dry run.
    if args.no_commit:
        print("⚠️ Dry-run mode (no changes committed)")
    else:
        conn.commit()

    conn.close()

    # Report the result of the import.
    print("\nSummary:")
    print(f"Inserted: {inserted}")
    print(f"Skipped : {skipped}")
    print(f"Failed  : {failed}")


def main():
    """Parse command-line arguments and load the selected TSV file."""
    parser = argparse.ArgumentParser(
        description="Insert TSV data into SQL table with conflict handling"
    )

    parser.add_argument("--file", required=True, help="Path to TSV file")
    parser.add_argument("--db", default=DATABASE_PATH, help="SQLite DB file path")
    parser.add_argument("--table", required=True, help="Target table name")

    parser.add_argument(
        "--mode",
        choices=["skip", "replace", "fail"],
        default="skip",
        help="Conflict handling mode (default: skip)",
    )

    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Dry run (do not commit changes)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-row status",
    )

    args = parser.parse_args()
    load_tsv(args)


if __name__ == "__main__":
    main()