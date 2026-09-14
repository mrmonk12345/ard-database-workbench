#!/bin/bash

# ====================
# CONFIG (edit here)
# ====================
read_flag="R1"        # R1 / R2 / all
type_flag="forward"   # forward / reverse / single

input_dir="data/samples/16s"
threads=16

# ====================
# SETUP
# ====================
mkdir -p qc/fastqc/{forward,reverse,single}

# ====================
# PATTERN
# ====================
pattern="*${read_flag}*"
if [[ "$read_flag" == "all" ]]; then
    pattern="*"
fi

# ====================
# RUN FASTQC
# ====================
fastqc -t $threads -o qc/fastqc/$type_flag $input_dir/$pattern.fastq.gz