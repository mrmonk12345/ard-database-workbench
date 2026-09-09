#!/usr/bin/env bash

source /home/ARO.local/collaboration/michalm_collab/envs/database/env_database.sh

PIPELINE_RUN_ID=8
REFERENCE="silva_r138"

echo "Uploading taxonomy for pipeline run ${PIPELINE_RUN_ID}"
echo "Reference: ${REFERENCE}"
echo "Taxonomy file: pipeline_runs/${PIPELINE_RUN_ID}/exported/silva_taxonomy.tsv"

python scripts/python/upload_taxonomy_to_database.py \
    --pipeline-run-id "${PIPELINE_RUN_ID}" \
    --reference "${REFERENCE}" \
    --taxonomy "pipeline_runs/${PIPELINE_RUN_ID}/exported/silva_taxonomy.tsv" \
    --db-path final_ARD_projects_latest.db
