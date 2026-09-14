. /data/bin/miniconda2/envs/qiime2-v2024.2.0/env_qiime2.sh

# Table
qiime tools export \
  --input-path results/16s/qiime_dada2_denoise_paired/16s_table.qza \
  --output-path exported

# Rep seqs
qiime tools export \
  --input-path results/16s/qiime_dada2_denoise_paired/16s_rep_seqs.qza \
  --output-path exported


# Taxonomy
qiime tools export \
  --input-path results/16s/qiime_diversity/16s_taxonomy.qza \
  --output-path exported
