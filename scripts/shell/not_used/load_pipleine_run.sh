#!/bin/bash
set -euo pipefail

PIPELINE_RUN_ID="$1"

EXPORT_DIR="pipeline_runs/${PIPELINE_RUN_ID}/exported"

python upload_asvs_fasta_to_database.py \
    --pipeline-run-id "${PIPELINE_RUN_ID}" \
    --fasta "${EXPORT_DIR}/dna-sequences.fasta"

python upload_feature_counts_to_database.py \
    --pipeline-run-id "${PIPELINE_RUN_ID}" \
    --table "${EXPORT_DIR}/feature-table.tsv"

python upload_taxonomy_to_database.py \
    --pipeline-run-id "${PIPELINE_RUN_ID}" \
    --taxonomy "${EXPORT_DIR}/taxonomy.tsv"

echo "Finished loading pipeline run ${PIPELINE_RUN_ID}"