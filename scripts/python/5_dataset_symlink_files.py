#!/usr/bin/env python3
import argparse
import sqlite3
import os
import sys

DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/final_ARD_projects_fixing_libraries.db"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"
DEFAULT_FILES_DIR = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_files/"

SQL = """
SELECT
	au.analysis_unit_id,
	auf.read1_path,
	auf.read2_path
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN analysis_unit_files auf
	ON au.analysis_unit_id = auf.analysis_unit_id 
WHERE adi.analysis_dataset_id = ? ;
"""


def main():
    parser = argparse.ArgumentParser(
        description="Create symlinks for FASTQ files"
    )

    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--files-dir", default=DEFAULT_FILES_DIR)
    parser.add_argument("--outdir-base", default=None)

    args = parser.parse_args()

    # checks
    if not os.path.exists(args.db):
        sys.exit(f"ERROR: database not found: {args.db}")

    if not os.path.isdir(args.files_dir):
        sys.exit(f"ERROR: files directory not found: {args.files_dir}")

    # ? output directory
    if args.outdir_base:
        outdir = os.path.join(
        args.outdir_base,
        str(args.dataset_id),
        "analysis_unit_files"
        )
    else:
        outdir = os.path.join(
        DEFAULT_OUTPUT_BASE,
        str(args.dataset_id),
        "analysis_unit_files"
        )
    os.makedirs(outdir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    rows = cur.execute(SQL, (args.dataset_id,)).fetchall()

    if not rows:
        sys.exit("ERROR: no files found")

    seen = set()
    count = 0

    for analysis_unit_id, fwd, rev in rows:

        if analysis_unit_id in seen:
            continue
        seen.add(analysis_unit_id)

        fwd_src = os.path.join(args.files_dir, fwd)
        rev_src = os.path.join(args.files_dir, rev)

        if not os.path.exists(fwd_src):
            sys.exit(f"ERROR: missing file: {fwd_src}")
        if not os.path.exists(rev_src):
            sys.exit(f"ERROR: missing file: {rev_src}")

        fwd_dest = os.path.join(outdir, fwd)
        rev_dest = os.path.join(outdir, rev)


        # create symlinks
        if not os.path.exists(fwd_dest):
            os.symlink(fwd_src, fwd_dest)

        if not os.path.exists(rev_dest):
            os.symlink(rev_src, rev_dest)

        count += 1

    conn.close()

    print(f"✅ Linked {count} samples ({count * 2} files)")
    print(f"📁 Output: {outdir}")


if __name__ == "__main__":
    main()
