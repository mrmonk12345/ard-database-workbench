#!/bin/bash

# ====================
# CONFIG
# ====================
input_dir="data/samples/16s"
threads=16

# Activate MultiQC environment
. /data/bin/miniconda2/envs/multiqc-v1.9/env_multiqc.sh

# ====================
# PROCESS FORWARD + REVERSE
# ====================
for type_flag in forward reverse
do
    if [[ "$type_flag" == "forward" ]]; then
        read_flag="R1"
    else
        read_flag="R2"
    fi

    echo "Processing $type_flag ($read_flag)..."

    # Create output directories
    mkdir -p qc/fastqc/$type_flag
    mkdir -p qc/multiqc/$type_flag

    # Run FastQC
    fastqc \
        -t $threads \
        -o qc/fastqc/$type_flag \
        "$input_dir"/*${read_flag}*.fastq.gz

    # Run MultiQC
    multiqc \
        qc/fastqc/$type_flag/ \
        -o qc/multiqc/$type_flag/

done

echo "All FastQC and MultiQC runs completed."