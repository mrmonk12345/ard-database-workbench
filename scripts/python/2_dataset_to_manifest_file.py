#!/usr/bin/env python3

import argparse
import sqlite3
import csv
import os
import sys


DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/final_ARD_projects_fixing_libraries.db"
DEFAULT_FASTQ_DIR = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_files/"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"


SQL = """
SELECT
    au.analysis_unit_name,
    auf.read1_path,
    auf.read2_path
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN analysis_unit_files auf
    ON au.analysis_unit_id = auf.analysis_unit_id
WHERE adi.analysis_dataset_id = ?
  AND auf.read1_path IS NOT NULL
  AND auf.read2_path IS NOT NULL;
"""


def write_tsv(path, header, rows):
    with open(path, "w") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")


def make_absolute(path, base_dir):
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(base_dir, path))


def main():
    parser = argparse.ArgumentParser(description="Create FASTQ manifest from DB")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--dataset-id", required=True, type=int)
    parser.add_argument("--fastq-dir", default=DEFAULT_FASTQ_DIR)
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

    # Connect to DB
    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    # ? qiime manifest
    rows = cur.execute(
        SQL, 
        (args.dataset_id,)
    ).fetchall()

    if not rows:
        sys.exit("ERROR: No data found!")

    # Process file paths
    manifest_rows = []
    for sample, r1, r2 in rows:
        r1_abs = make_absolute(r1, args.fastq_dir)
        r2_abs = make_absolute(r2, args.fastq_dir)
        manifest_rows.append([sample, r1_abs, r2_abs])

    # Header and file writing
    manifest_header = ["sample-id", "forward-absolute-filepath", "reverse-absolute-filepath"]
    manifest_path = os.path.join(outdir, "qiime_manifest.tsv")
    
    write_tsv(manifest_path, manifest_header, manifest_rows)

    conn.close()

    print(f"? Manifest written to: {manifest_path}")
    print("? Done.")


if __name__ == "__main__":
    main()