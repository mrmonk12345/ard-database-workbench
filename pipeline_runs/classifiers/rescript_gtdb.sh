. /data/bin/miniconda2/envs/qiime2-v2024.2.0/env_qiime2.sh;

qiime rescript get-gtdb-data \
  --p-version '214.0' \
  --p-db-type 'SpeciesReps' \
  --p-domain 'Both' \
  --o-gtdb-taxonomy gtdb-214-tax.qza \
  --o-gtdb-sequences gtdb-214-seqs.qza