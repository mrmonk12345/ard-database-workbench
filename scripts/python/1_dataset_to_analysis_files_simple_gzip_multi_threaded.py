#!/usr/bin/env python3
import argparse
import sqlite3
import os
import sys
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_DB = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/final_ARD_projects_fixing_libraries.db"
DEFAULT_FASTQ_DIR = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/raw_reads/"
DEFAULT_OUTPUT_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_files/"

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
JOIN libraries l
    ON l.library_id = au.library_id
JOIN sequencing_outputs so
    ON au.sequencing_run_id = so.sequencing_run_id
    AND l.sample_id = so.sample_id
WHERE adi.analysis_dataset_id = ?
  AND so.fastq1 IS NOT NULL
  AND so.fastq2 IS NOT NULL
  AND so.sequencing_run_id IS NOT NULL
  AND so.amplicon_type_id IS NOT NULL;
"""
GET_PROJECT_ID_SQL = """
SELECT sr.project_id
FROM sequencing_runs sr
JOIN analysis_datasets ad ON sr.sequencing_run_id = ad.sequencing_run_id
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
    with open(dst, "wb") as out_f:
        subprocess.run(
            ["pigz", "-p", str(threads), "-c", src],
            stdout=out_f,
            check=True
        )

def copy_gz(src, dst):
    shutil.copy2(src, dst)

# ? worker function (runs in parallel)
def process_sample(row, args, outdir, project_id):
    analysis_unit_id, analysis_unit_name, sequencing_output_id, fwd, rev = row

    fwd_path = os.path.join(args.fastq_dir, project_id, fwd)
    rev_path = os.path.join(args.fastq_dir, project_id, rev)

    if not os.path.exists(fwd_path):
        raise FileNotFoundError(f"Missing file: {fwd_path}")
    if not os.path.exists(rev_path):
        raise FileNotFoundError(f"Missing file: {rev_path}")

    fwd_out = os.path.join(outdir, f"{analysis_unit_name}_R1.fastq.gz")
    rev_out = os.path.join(outdir, f"{analysis_unit_name}_R2.fastq.gz")


    # --- skip if already exists ---
    if os.path.exists(fwd_out) and os.path.exists(rev_out):
        print(f"Skipping {analysis_unit_name} (already exists)")
        return (
            analysis_unit_id,
            sequencing_output_id,
            os.path.basename(fwd_out),
            os.path.basename(rev_out)
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

    return (
        analysis_unit_id,
        sequencing_output_id,
        os.path.basename(fwd_out),
        os.path.basename(rev_out)
    )

def main():
    parser = argparse.ArgumentParser(
        description="Create gzipped FASTQ files (multithreaded)"
    )

    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--fastq-dir", default=DEFAULT_FASTQ_DIR)
    parser.add_argument("--outdir", default=None)

    parser.add_argument("--threads", type=int, default=4,
                        help="Threads per pigz process")

    parser.add_argument("--workers", type=int, default=2,
                        help="Number of parallel samples")

    args = parser.parse_args()

    if not os.path.exists(args.db):
        sys.exit(f"ERROR: database not found: {args.db}")

    if not os.path.isdir(args.fastq_dir):
        sys.exit(f"ERROR: FASTQ directory not found: {args.fastq_dir}")

    outdir = args.outdir or DEFAULT_OUTPUT_BASE
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

    # ? deduplicate
    seen = set()
    filtered = []
    for row in rows:
        if row[0] in seen:
            continue
        seen.add(row[0])
        filtered.append(row)

    results = []

    # ? parallel execution
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(process_sample, row, args, outdir, project_id)
                   for row in filtered]

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"ERROR: {e}")
                sys.exit(1)

    # ? single-thread DB writes
    for analysis_unit_id, sequencing_output_id, r1, r2 in results:
        cur.execute(
            WRITE_FILES_DATABASE_SQL,
            (analysis_unit_id, sequencing_output_id, r1, r2)
        )

    conn.commit()
    conn.close()

    count = len(results)
    print(f"? Processed {count} samples ({count * 2} files)")
    print(f"?? Output: {outdir}")

if __name__ == "__main__":
    main()