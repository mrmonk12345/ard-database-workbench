#!/usr/bin/env python3
"""Copy dataset metadata and FASTQ links to a pipeline run directory."""

import argparse
import os
import sys
import shutil
import glob

DEFAULT_PIPELINE_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/pipeline_runs/"
DEFAULT_DATASET_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"


def main():
    """Prepare a pipeline run directory from an analysis dataset."""
    parser = argparse.ArgumentParser(
        description="Copy files to pipeline run"
    )

    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--dataset-dir-base", default=DEFAULT_DATASET_BASE)
    parser.add_argument("--pipeline-dir-base", default=DEFAULT_PIPELINE_BASE)
    parser.add_argument("--pipeline-name", default=None)

    args = parser.parse_args()


    # Use the pipeline name when provided; otherwise use the dataset ID.
    if args.pipeline_name:
        outdir = os.path.join(
        args.pipeline_dir_base,
        str(args.pipeline_name)
        )
    else:
        outdir = os.path.join(
        args.pipeline_dir_base,
        str(args.dataset_id)
        )
    os.makedirs(outdir, exist_ok=True)

    # Locate the source dataset directory.
    indir = os.path.join(
        args.dataset_dir_base,
        str(args.dataset_id)
        )

    # Map dataset files to their locations in the pipeline directory.
    copies = [
        ("qiime_manifest.tsv", "data/16s_file_metadata.tsv"),
        ("sample_metadata.tsv", "data/16s_sample_metadata_file.tsv"),
        ("amplicon_metadata.tsv", "amplicon_metadata.tsv")
    ]

    # Copy the metadata files to the pipeline run directory.
    for src_name, dst_rel in copies:
        src = os.path.join(indir, src_name)
        dst = os.path.join(outdir, dst_rel)

        # Ensure the destination folder exists.
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        shutil.copy2(src, dst)

        print(f"Copied {src} -> {dst}")


    # Link all analysis FASTQ files into the pipeline samples directory.
    src_pattern = os.path.join(indir, "analysis_unit_files", "*")
    dst_dir = os.path.join(outdir, "data", "samples", "16s")

    os.makedirs(dst_dir, exist_ok=True)

    for file_path in glob.glob(src_pattern):
        dst = os.path.abspath(os.path.join(dst_dir, os.path.basename(file_path)))
        print(dst)
        real_path = os.path.realpath(file_path)

        # Replace an existing file or symlink.
        if os.path.exists(dst):
          os.remove(dst)
        os.symlink(real_path, dst)

        print(f"Linked {real_path} -> {dst}")

if __name__ == "__main__":
    main()