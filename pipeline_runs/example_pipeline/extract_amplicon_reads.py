#!/usr/bin/env python3
"""
extract_amplicon_reads.py

Extracts amplicon-specific reads from a QIIME 2 reference sequence artifact (.qza)
using primer sequences and expected amplicon lengths parsed from a metadata TSV.

Usage:
    python extract_amplicon_reads.py \
        --input-seqs gtdb-220-seqs.qza \
        --metadata amplicon_metadata.tsv \
        --output-seqs gtdb-220-v4-seqs.qza \
        --n-jobs 8
"""

import argparse
import subprocess
import sys
from pathlib import Path
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run QIIME 2 extract-reads using primer parameters from a metadata TSV."
    )
    parser.add_argument(
        "--input-seqs",
        type=Path,
        default="../classifiers/gtdb_classifier_r220.qza",
        help="Path to input QIIME 2 reference sequences (.qza)",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default="amplicon_metadata.tsv",
        help="Path to amplicon metadata TSV file",
    )
    parser.add_argument(
        "--output-seqs",
        type=Path,
        default="gtdb-220-seqs.qza",
        help="Path to save extracted reference reads (.qza)",
    )
    parser.add_argument(
        "--n-jobs",
        type=int,
        default=8,
        help="Number of CPU cores/threads for parallel processing (default: 8)",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=100,
        help="Allowed length variation +/- around expected amplicon length (default: 100)",
    )
    return parser.parse_args()


def extract_reads(input_seqs: Path, metadata_tsv: Path, output_seqs: Path, n_jobs: int, padding: int):
    # Read metadata table
    df = pd.read_csv(metadata_tsv, sep="\t")

    if df.empty:
        raise ValueError("Metadata TSV is empty.")

    # Extract required fields from first row
    row = df.iloc[0]
    f_primer = str(row["f_sequence"]).strip()
    r_primer = str(row["r_sequence"]).strip()
    amplicon_len = int(row["amplicon_length"])

    # Calculate min and max lengths dynamically based on expected length and padding
    min_len = max(50, amplicon_len - padding)
    max_len = amplicon_len + padding

    print(f"Loaded primers from metadata:")
    print(f"  Forward Primer ({row.get('f_name', 'F')}): {f_primer}")
    print(f"  Reverse Primer ({row.get('r_name', 'R')}): {r_primer}")
    print(f"  Expected Length: {amplicon_len} bp (Min: {min_len}, Max: {max_len})")

    # Construct QIIME 2 CLI command
    cmd = [
        "qiime",
        "feature-classifier",
        "extract-reads",
        "--i-sequences",
        str(input_seqs),
        "--p-f-primer",
        f_primer,
        "--p-r-primer",
        r_primer,
        "--p-min-length",
        str(min_len),
        "--p-max-length",
        str(max_len),
        "--p-n-jobs",
        str(n_jobs),
        "--o-reads",
        str(output_seqs),
    ]

    print("\nExecuting command:")
    print(" ".join(cmd))

    # Execute system call
    try:
        subprocess.run(cmd, check=True)
        print(f"\nSuccessfully extracted reads to: {output_seqs}")
    except subprocess.CalledProcessError as e:
        print(f"\nError executing QIIME 2 command: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    extract_reads(
        input_seqs=args.input_seqs,
        metadata_tsv=args.metadata,
        output_seqs=args.output_seqs,
        n_jobs=args.n_jobs,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()