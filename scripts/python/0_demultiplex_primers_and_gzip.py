#!/usr/bin/env python3

"""
0_demultiplex_primers_and_gzip.py

Demultiplex raw sequencing FASTQ files by dataset amplicon primers (paired-end),
compress outputs with gzip via Cutadapt, and write entries into analysis_unit_files.
"""

import argparse
import sqlite3
import tempfile
import subprocess
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import (
    DATABASE_PATH,
    RAW_READS_PATH,
    ANALYSIS_FILES_PATH,
)


# -----------------------------------------------------------------------------
# SQL Queries
# -----------------------------------------------------------------------------

# Fetch raw FASTQ inputs for the specified dataset ID
GET_INPUT_SAMPLES_SQL = """
SELECT
    au.analysis_unit_id,
    au.analysis_unit_name,
    so.sequencing_output_id,
    so.project_id,
    so.fastq1,
    so.fastq2
FROM analysis_datasets ad
JOIN analysis_units au
    ON ad.analysis_dataset_id = au.analysis_dataset_id
JOIN libraries l
    ON l.library_id = au.library_id
JOIN sequencing_outputs so
    ON l.sample_id = so.sample_id
WHERE ad.analysis_dataset_id = ?
  AND so.fastq1 IS NOT NULL
  AND so.fastq2 IS NOT NULL
  AND so.sequencing_run_id = ad.sequencing_run_id;
"""

# Fetch forward and reverse primer sequences for the dataset
GET_DATASET_PRIMERS_SQL = """
SELECT DISTINCT
    at.amplicon_type_id,
    at.f_sequence,
    at.r_sequence
FROM amplicon_types at
JOIN analysis_datasets ad 
    ON ad.amplicon_type_id = at.amplicon_type_id
WHERE ad.analysis_dataset_id = ?
  AND at.f_sequence IS NOT NULL;
"""

# Populate or update records in analysis_unit_files
WRITE_ANALYSIS_FILES_SQL = """
INSERT INTO analysis_unit_files (
    analysis_unit_id,
    sequencing_output_id,
    read1_path,
    read2_path,
    amplicon_separating_done,
    gzip_done
) VALUES (?, ?, ?, ?, 1, 1)
ON CONFLICT(analysis_unit_id) DO UPDATE SET
    sequencing_output_id = excluded.sequencing_output_id,
    read1_path = excluded.read1_path,
    read2_path = excluded.read2_path,
    amplicon_separating_done = 1,
    gzip_done = 1;
"""


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def write_dataset_primer_fastas(conn, dataset_id):
    """
    Query forward/reverse primers for the dataset and write them to temporary
    FASTA files required by Cutadapt.
    """
    rows = conn.execute(GET_DATASET_PRIMERS_SQL, (dataset_id,)).fetchall()

    if not rows:
        sys.exit(f"ERROR: No primers found for dataset ID {dataset_id}")

    tmp_fwd = tempfile.NamedTemporaryFile(mode="w", suffix="_fwd.fa", delete=False)
    tmp_rev = tempfile.NamedTemporaryFile(mode="w", suffix="_rev.fa", delete=False)

    for at_id, f_seq, r_seq in rows:
        header = f">AT{at_id}\n"
        if f_seq:
            tmp_fwd.write(header)
            tmp_fwd.write(f"^{f_seq.strip().upper()}\n")
        if r_seq:
            tmp_rev.write(header)
            tmp_rev.write(f"^{r_seq.strip().upper()}\n")

    tmp_fwd.close()
    tmp_rev.close()

    return tmp_fwd.name, tmp_rev.name


def demultiplex_sample(row, args, outdir, fwd_fasta, rev_fasta):
    """
    Process a single analysis unit: run Cutadapt to demultiplex paired FASTQ
    files and return output metadata for database insertion.
    """
    (
        analysis_unit_id,
        analysis_unit_name,
        sequencing_output_id,
        project_id,
        fastq1,
        fastq2,
    ) = row

    # Full paths to raw input FASTQ files
    fwd_path = os.path.join(args.fastq_dir, str(project_id), fastq1)
    rev_path = os.path.join(args.fastq_dir, str(project_id), fastq2)

    if not os.path.exists(fwd_path) or not os.path.exists(rev_path):
        raise FileNotFoundError(f"Missing raw FASTQs for {analysis_unit_name}: {fwd_path}")

    # Output file paths matching Script 1 naming convention
    r1_filename = f"{analysis_unit_name}_R1.fastq.gz"
    r2_filename = f"{analysis_unit_name}_R2.fastq.gz"

    out_r1 = os.path.join(outdir, r1_filename)
    out_r2 = os.path.join(outdir, r2_filename)

    # Cutadapt command for paired-end demultiplexing and automatic gzip compression
    cmd = [
        "cutadapt",
        "--action=none",
        "-e", "0.10",
        "-O", "15",
        "-j", str(args.threads),
        "-g", f"file:{fwd_fasta}",
        "-G", f"file:{rev_fasta}",
        "-o", out_r1,
        "-p", out_r2,
        fwd_path,
        rev_path,
    ]

    print(f"Demultiplexing: {analysis_unit_name}")
    subprocess.run(cmd, check=True)

    return (
        analysis_unit_id,
        sequencing_output_id,
        r1_filename,
        r2_filename,
    )


# -----------------------------------------------------------------------------
# Main Workflow
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Demultiplex raw FASTQ outputs by primers and record analysis unit files."
    )

    parser.add_argument("--db", default=DATABASE_PATH, help="Path to SQLite database")
    parser.add_argument("--dataset-id", type=int, required=True, help="Target analysis dataset ID")
    parser.add_argument("--fastq-dir", default=RAW_READS_PATH, help="Directory containing raw FASTQs")
    parser.add_argument("--outdir", default=ANALYSIS_FILES_PATH, help="Output directory for analysis files")
    parser.add_argument("--threads", type=int, default=4, help="Threads per Cutadapt job")
    parser.add_argument("--workers", type=int, default=2, help="Number of parallel sample workers")

    args = parser.parse_args()

    # Verify database file existence
    if not os.path.exists(args.db):
        sys.exit(f"ERROR: Database file not found: {args.db}")

    os.makedirs(args.outdir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    # Query input sequencing outputs
    rows = cur.execute(GET_INPUT_SAMPLES_SQL, (args.dataset_id,)).fetchall()

    if not rows:
        sys.exit(f"ERROR: No matching raw FASTQs found for dataset ID {args.dataset_id}")

    # Generate temporary primer FASTA files
    fwd_fasta, rev_fasta = write_dataset_primer_fastas(conn, args.dataset_id)

    results = []

    try:
        # Process samples in parallel threads
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [
                executor.submit(
                    demultiplex_sample,
                    row,
                    args,
                    args.outdir,
                    fwd_fasta,
                    rev_fasta,
                )
                for row in rows
            ]

            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"ERROR processing sample: {e}")
                    sys.exit(1)

        # Write generated file paths back to the database in a single thread
        for unit_id, seq_out_id, r1_name, r2_name in results:
            cur.execute(
                WRITE_ANALYSIS_FILES_SQL,
                (unit_id, seq_out_id, r1_name, r2_name),
            )

        conn.commit()
        print(f"Successfully demultiplexed and registered {len(results)} analysis units.")

    finally:
        # Clean up temporary primer FASTA files
        for fasta_file in (fwd_fasta, rev_fasta):
            if os.path.exists(fasta_file):
                os.remove(fasta_file)

        conn.close()


if __name__ == "__main__":
    main()
