#!/usr/bin/env python3
import argparse
import sqlite3
import os
import sys

DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/final_ARD_projects_fixing_libraries.db"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"

SQL = """
SELECT DISTINCT
    at.*
FROM analysis_datasets ad
JOIN analysis_units au
    ON ad.analysis_dataset_id = au.analysis_dataset_id
JOIN libraries l
  ON au.library_id = l.library_id
JOIN amplicon_types at
    ON l.amplicon_type_id = at.amplicon_type_id
WHERE au.analysis_dataset_id = ?
"""


def write_tsv(path, header, rows):
    with open(path, "w") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Create metadata files for dataset"
    )
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--outdir-base", default=None)

    args = parser.parse_args()

    # ? checks
    if not os.path.exists(args.db):
        sys.exit(f"ERROR: database not found: {args.db}")

    # ? output dir (match gzip script structure)
    if args.outdir_base:
        outdir = os.path.join(
        args.outdir_base,
        str(args.dataset_id)
        )
    else:
        outdir = os.path.join(
            DEFAULT_OUTPUT_BASE,
            str(args.dataset_id),
        )

    os.makedirs(outdir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    # ? amplicon metadata
    amplicon_rows = cur.execute(
        SQL,
        (args.dataset_id,)
    ).fetchall()

    if not amplicon_rows:
        print("WARNING: no amplicon metadata found")

    # dynamic header from DB
    amplicon_header = [desc[0] for desc in cur.description]

    amplicon_path = os.path.join(outdir, "amplicon_metadata.tsv")
    write_tsv(amplicon_path, amplicon_header, amplicon_rows)
    
    print(f"? Amplicon metadata: {amplicon_path}")
    print("? Done.")

if __name__ == "__main__":
    main()