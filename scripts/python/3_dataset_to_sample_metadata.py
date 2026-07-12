#!/usr/bin/env python3
import argparse
import sqlite3
import os
import sys

DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/final_ARD_projects_fixing_libraries.db"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"

SQL = """
SELECT
    au.analysis_unit_name,
    s.sample_id,
    s.project_id,
    s.treatment_id,
    t.name AS treatment_name,
    au.label,
    s.label,
    s.time_since_planting
FROM analysis_datasets ad
JOIN analysis_units au
    ON ad.analysis_dataset_id = au.analysis_dataset_id
JOIN libraries l
    ON l.library_id = au.library_id
JOIN samples s
    ON s.sample_id = l.sample_id
JOIN treatments t
    ON t.treatment_id = s.treatment_id
WHERE au.analysis_dataset_id = ? ;
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

    # ? sample metadata
    sample_rows = cur.execute(
        SQL,
        (args.dataset_id,)
    ).fetchall()

    if not sample_rows:
        sys.exit("ERROR: no sample metadata found")

    sample_header = ["sample_name", "sample_id", "project_id", "treatment_id", "treatment_name", "analysis_unit_label", "sample_label",                      "time_since_planting"]

    sample_path = os.path.join(outdir, "sample_metadata.tsv")
    write_tsv(sample_path, sample_header, sample_rows)
    
    print(f"? Sample metadata: {sample_path}")
    print("? Done.")

if __name__ == "__main__":
    main()