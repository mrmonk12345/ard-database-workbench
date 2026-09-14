#!/bin/bash

# activate env
. /data/bin/miniconda2/envs/multiqc-v1.9/env_multiqc.sh

type_flag="forward"  # forward / reverse / single

# run multiqc
multiqc qc/fastqc/$type_flag/ -o qc/multiqc/$type_flag/