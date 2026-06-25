#!/usr/bin/env python3
import argparse
import os
import sys
import shutil
import glob

DEFAULT_PIPELINE_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/pipeline_runs/"
DEFAULT_DATASET_BASE = "/home/ARO.local/michaelr/Projects/db_fixing_libraries/analysis_datasets/"


def main():
    parser = argparse.ArgumentParser(
        description="Copy files to pipeline run"
    )

    parser.add_argument("--dataset-id", type=int, required=True)
    parser.add_argument("--dataset-dir-base", default=DEFAULT_DATASET_BASE)
    parser.add_argument("--pipeline-dir-base", default=DEFAULT_PIPELINE_BASE)
    parser.add_argument("--pipeline-name", default=None)

    args = parser.parse_args()


    # ? output directory
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

    # ? input directory
    indir = os.path.join(
        args.dataset_dir_base,
        str(args.dataset_id)
        )


    copies = [
        ("qiime_manifest.tsv", "data/16s_file_metadata.tsv"),
        ("sample_metadata.tsv", "data/16s_sample_metadata_file.tsv"),
        ("amplicon_metadata.tsv", "amplicon_metadata.tsv")
    ]

    # ✅ copy metadata files
    for src_name, dst_rel in copies:
        src = os.path.join(indir, src_name)
        dst = os.path.join(outdir, dst_rel)

        # ensure destination folder exists
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        shutil.copy2(src, dst)

        print(f"Copied {src} -> {dst}")


    # ✅ copy multiple files (wildcard)

    src_pattern = os.path.join(indir, "analysis_unit_files", "*")
    dst_dir = os.path.join(outdir, "data", "samples", "16s")

    os.makedirs(dst_dir, exist_ok=True)

    for file_path in glob.glob(src_pattern):
        dst = os.path.join(dst_dir, os.path.basename(file_path))

        real_path = os.path.realpath(file_path)

        if os.path.exists(dst):
          os.remove(dst)
        os.symlink(real_path, dst)

        print(f"Linked {real_path} -> {dst}")

if __name__ == "__main__":
    main()