#!/usr/bin/env bash


# ==============================================================================
# ENVIRONMENTS
# ==============================================================================

source /data/bin/miniconda2/envs/qiime2-v2024.2.0/env_qiime2.sh
source /data/bin/miniconda2/envs/pandas-v2.3.3/env_pandas.sh

set -euo pipefail
# ==============================================================================
# CONFIGURATION
# ==============================================================================

INPUT_SEQS="../classifiers/silva-138-dna-seqs.qza"
INPUT_TAX="../classifiers/silva-138-tax.qza"
METADATA_TSV="amplicon_metadata.tsv"
ASV_READS="results/16s/qiime_dada2_denoise_paired/16s_rep_seqs.qza"
N_JOBS=8

# Directories
RESULTS="results/new_method_taxonomy"
EXPORTED="exported"

mkdir -p "${RESULTS}"
mkdir -p "${EXPORTED}"

# Intermediate & Output Files
EXTRACTED_SEQS="${RESULTS}/silva-138-extracted-seqs.qza"
TRAINED_CLASSIFIER="${RESULTS}/silva-138-classifier.qza"
FINAL_TAXONOMY="${RESULTS}/silva-138-taxonomy.qza"
FINAL_TAXONOMY_TSV="${EXPORTED}/silva_taxonomy.tsv"

# ==============================================================================
# PIPELINE EXECUTION
# ==============================================================================

echo "========================================================================"
echo "Step 2: Trimming GTDB Sequences using Python helper script"
echo "========================================================================"

python3 extract_amplicon_reads.py \
    --input-seqs "${INPUT_SEQS}" \
    --metadata "${METADATA_TSV}" \
    --output-seqs "${EXTRACTED_SEQS}" \
    --n-jobs "${N_JOBS}"

echo
echo "========================================================================"
echo "Step 3: Training Naive Bayes Classifier on extracted GTDB reads"
echo "========================================================================"

qiime feature-classifier fit-classifier-naive-bayes \
    --i-reference-reads "${EXTRACTED_SEQS}" \
    --i-reference-taxonomy "${INPUT_TAX}" \
    --o-classifier "${TRAINED_CLASSIFIER}"

echo
echo "========================================================================"
echo "Step 4: Classifying ASVs against trained GTDB classifier"
echo "========================================================================"

qiime feature-classifier classify-sklearn \
    --i-reads "${ASV_READS}" \
    --i-classifier "${TRAINED_CLASSIFIER}" \
    --p-read-orientation same \
    --p-n-jobs "${N_JOBS}" \
    --o-classification "${FINAL_TAXONOMY}"

echo
echo "========================================================================"
echo "Exporting taxonomy artifact to TSV table"
echo "========================================================================"

qiime tools export \
    --input-path "${FINAL_TAXONOMY}" \
    --output-path tmp_export_dir

mv tmp_export_dir/taxonomy.tsv "${FINAL_TAXONOMY_TSV}"
rmdir tmp_export_dir

echo
echo "Pipeline completed successfully!"
echo "Classifier: ${TRAINED_CLASSIFIER}"
echo "Taxonomy artifact: ${FINAL_TAXONOMY}"
echo "Taxonomy table: ${FINAL_TAXONOMY_TSV}"
