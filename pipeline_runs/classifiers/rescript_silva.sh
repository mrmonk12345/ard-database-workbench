. /data/bin/miniconda2/envs/qiime2-v2024.2.0/env_qiime2.sh

qiime rescript get-silva-data \
    --p-version 138 \
    --p-target SSURef_NR99 \
    --o-silva-taxonomy silva-138-tax.qza \
    --o-silva-sequences silva-138-seqs.qza

qiime rescript reverse-transcribe \
    --i-rna-sequences silva-138-seqs.qza \
    --o-dna-sequences silva-138-dna-seqs.qza