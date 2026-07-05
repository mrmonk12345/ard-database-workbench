#!/usr/bin/env python3
import argparse
import sqlite3
import os
import sys
import subprocess
import shutil

DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_collab_copy/Projects_DB/final_ARD_projects.db"
DEFAULT_FASTQ_DIR = "/home/ARO.local/michaelr/Projects/db_collab_copy/Projects_DB/raw_reads/"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_collab_copy/Projects_DB/analysis_files"

MAKE_ANALYSIS_FILES_SQL = """
SELECT
    au.analysis_unit_id,
    au.analysis_unit_name,
    so.sequencing_output_id,
    so.fastq1,
    so.fastq2
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN sequencing_outputs so
    ON au.sequencing_run_id = so.sequencing_run_id
   AND au.library_id = so.library_id
   AND au.amplicon_type_id = so.amplicon_type_id
JOIN libraries l
    ON l.library_id = au.library_id
JOIN samples s
    ON s.sample_id = l.sample_id
WHERE adi.analysis_dataset_id = ?
  AND so.fastq1 IS NOT NULL
  AND so.fastq2 IS NOT NULL;
"""

GET_PROJECT_ID_SQL = """
SELECT sr.project_id
FROM sequencing_runs sr
JOIN analysis_datasets ad
    ON sr.sequencing_run_id = ad.sequencing_run_id
WHERE ad.analysis_dataset_id = ?
"""

WRITE_FILES_DATABASE_SQL = """
INSERT INTO analysis_unit_files (
    analysis_unit_id,
    sequencing_output_id,
    read1_path,
    read2_path,
    gzip_done
) VALUES (?, ?, ?, ?, 1)
ON CONFLICT(analysis_unit_id) DO UPDATE SET
    sequencing_output_id = excluded.sequencing_output_id,
    read1_path = excluded.read1_path,
    read2_path = excluded.read2_path,
    gzip_done = 1;


"""

def gzip_file(src, dst, threads):
    """Compress using pigz"""
    with open(dst, "wb") as out_f:
        subprocess.run(
            ["pigz", "-p", str(threads), "-c", src],
            stdout=out_f,
            check=True
        )


def copy_gz(src, dst):
    """Copy already gzipped file"""
    shutil.copy2(src, dst)


def main():
    parser = argparse.ArgumentParser(
        description="Create gzipped FASTQ files (sequential, pigz)"
    )

    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--fastq-dir", default=DEFAULT_FASTQ_DIR)
    parser.add_argument("--outdir", default=None)

    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="Threads for pigz per file"
    )

    args = parser.parse_args()

    # ? checks
    if not os.path.exists(args.db):
        sys.exit(f"ERROR: database not found: {args.db}")

    if not os.path.isdir(args.fastq_dir):
        sys.exit(f"ERROR: FASTQ directory not found: {args.fastq_dir}")

    # ? output directory
    if args.outdir:
        outdir = args.outdir
    else:
        outdir = DEFAULT_OUTPUT_BASE


    os.makedirs(outdir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    project_row = cur.execute(GET_PROJECT_ID_SQL, (args.dataset_id,)).fetchone()

    if not project_row:
        sys.exit("ERROR: project_id not found")

    project_id = str(project_row[0])

    rows = cur.execute(MAKE_ANALYSIS_FILES_SQL, (args.dataset_id,)).fetchall()

    if not rows:
        sys.exit("ERROR: no FASTQs found")

    seen = set()
    count = 0

    for analysis_unit_id, analysis_unit_name, sequencing_output_id, fwd, rev in rows:

        # skip duplicates
        if analysis_unit_id in seen:
            continue
        seen.add(analysis_unit_id)

        fwd_path = os.path.join(args.fastq_dir, project_id, fwd)
        rev_path = os.path.join(args.fastq_dir, project_id, rev)


        if not os.path.exists(fwd_path):
            sys.exit(f"ERROR: missing file: {fwd_path}")
        if not os.path.exists(rev_path):
            sys.exit(f"ERROR: missing file: {rev_path}")

        # QIIME-compliant names
        fwd_out = os.path.join(
            outdir, f"{analysis_unit_name}_R1.fastq.gz"
        )
        rev_out = os.path.join(
            outdir, f"{analysis_unit_name}_R2.fastq.gz"
        )

        print(f"Processing {analysis_unit_name}")

        # forward
        if fwd.endswith(".gz"):
            copy_gz(fwd_path, fwd_out)
        else:
            gzip_file(fwd_path, fwd_out, args.threads)

        # reverse
        if rev.endswith(".gz"):
            copy_gz(rev_path, rev_out)
        else:
            gzip_file(rev_path, rev_out, args.threads)

            
        # ? insert into DB
        cur.execute(
            WRITE_FILES_DATABASE_SQL,
            (
                analysis_unit_id,
                sequencing_output_id,
                os.path.basename(fwd_out),
                os.path.basename(rev_out),
            )
            )

        count += 1
        

    conn.commit()
    conn.close()
    print(f"? Processed {count} samples ({count * 2} files)")
    print(f"?? Output: {outdir}")

    
if __name__ == "__main__":
    main()