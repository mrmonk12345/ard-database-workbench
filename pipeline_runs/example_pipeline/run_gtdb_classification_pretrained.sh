#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Path to your downloaded pre-trained GTDB classifier artifact
PRETRAINED_CLASSIFIER="../classifiers/gtdb_classifier_r220.qza"  # Update filename/path if needed

# Path to your query ASVs artifact
ASV_READS="rep-seqs.qza"                          

# Number of CPU threads/cores to use
N_JOBS=8                                          

# Output filenames
FINAL_TAXONOMY="gtdb-taxonomy.qza"        
FINAL_TAXONOMY_TSV="gtdb_taxonomy.tsv"    

# ==============================================================================
# EXECUTION: STEP 4 ONLY
# ==============================================================================

echo "========================================================================"
echo "Classifying ASVs using pre-trained GTDB classifier (${PRETRAINED_CLASSIFIER})"
echo "========================================================================"
qiime feature-classifier classify-sklearn \
    --i-reads "${ASV_READS}" \
    --i-classifier "${PRETRAINED_CLASSIFIER}" \
    --p-n-jobs "${N_JOBS}" \
    --o-classification "${FINAL_TAXONOMY}"

echo -e "\n========================================================================"
echo "Exporting taxonomy artifact to TSV table"
echo "========================================================================"
qiime tools export \
    --input-path "${FINAL_TAXONOMY}" \
    --output-path export_dir

mv export_dir/taxonomy.tsv "${FINAL_TAXONOMY_TSV}"
rmdir export_dir

echo -e "\nClassification completed successfully!"
echo "Final classification saved to: ${FINAL_TAXONOMY} and ${FINAL_TAXONOMY_TSV}"