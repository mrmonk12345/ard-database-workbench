#!/bin/bash

#Load Envrioments on HPC

#. /data/bin/miniconda2/envs/qiime2-v2022.2/env_qiime2.sh

. /data/bin/miniconda2/envs/qiime2-v2024.2.0/env_qiime2.sh

. /data/bin/miniconda2/envs/snakemake-v7.19.1/env_snakemake.sh

#INPUT parameters

#cores to input in hpc run of script

CORES=24

APLICON_TYPE="16s"

#For DADA 

#16s:

#mandatory

TRIM_LEFT_F=17

TRIM_LEFT_R=20 

#change only if dada fails, by order

#1. change to make a shorter overlap ( (--p-trunc-len-f + --p-trunc-len-r) -  min_merged_read_length >= 4 )

TRUNC_LEN_F=275

TRUNC_LEN_R=229

#2. change to lower vaule

P_MIN_OVERLAP=12 

#3. chage to higher value

P_MAX_EE_F=2.0

P_MAX_EE_R=2.0

#--p-max-ee-f NUMBER     Forward reads with number of expected errors higher
#than this value will be discarded.    [default: 2.0]
#--p-max-ee-r NUMBER     Reverse reads with number of expected errors higher
#than this value will be discarded.    [default: 2.0]
#--p-min-overlap INTEGER The minimum length of the overlap required for
#Range(4, None)        merging the forward and reverse reads. [default: 12]

#ITS:

#mandatory - this setup instructs dada2 to only preform merge part

#TRIM_LEFT_F=0

#TRIM_LEFT_R=0

#TRUNC_LEN_F=0

#TRUNC_LEN_R=0

#change only if dada fails, by order

#1. change to lower vaule

#P_MIN_OVERLAP=12

#2. chage to higher value

#P_MAX_EE_F=2.0

#P_MAX_EE_R=2.0

CONFIG_DADA="trim_left_f=$TRIM_LEFT_F trim_left_r=$TRIM_LEFT_R trunc_len_f=$TRUNC_LEN_F trunc_len_r=$TRUNC_LEN_R p_max_ee_f=$P_MAX_EE_F p_max_ee_r=$P_MAX_EE_R p_min_overlap=$P_MIN_OVERLAP" 

#update after dada2 part 

SAMPLING_DEPTH=10 

MAX_DEPTH=10 

# update for ANCOM 

P_LEVEL=4

TREATMENT="treatment"

CON_IN_COLUMNS="KARKOM"

CON_P_WHERE_COLUMNS="'KARKOM_NO_BSFF','KARKOM_BSFF'"

TREATMENT_IN_COLUMNS="$TREATMENT""_""$CON_IN_COLUMNS"

CONFIG="--config cores=$CORES aplicon_type="$APLICON_TYPE" p_level=$P_LEVEL treatment="$TREATMENT" con_in_columns="$CON_IN_COLUMNS" con_p_where_columns="$CON_P_WHERE_COLUMNS" sampling_depth="$SAMPLING_DEPTH" max_depth="$MAX_DEPTH""


#The workflow assumes:

#1. data and related files are separted by primer type, 16s and ITS

#2. Primer specific classifier, 16s and ITS 

#3. Length of farrowed (F) and reverse (R) Primer  and expected product length (min_merged_read_length)

#4. Sample_metadata_file and file_metadata are created from provided templates/exmpales.

#Run data/create_16s_file_metadata_from_template.sh to obtain 16s_file_metadata

#5. dada2 denosie-pared paramets are determined from fastqc (multiqc) (external script)

#determine parametres for dada2 denosie-pared.

#for 16s(example: forward sequencing 341F, reverse 806R.

#the min_merged_read (expected product length is

#(min_merged_read) = R - F + 1 = 806 - 341 + 1 =  466 # This includes 5' primes

# --p-trunc-len-f,  --p-trunc-len-r to staify :

#(--p-trunc-len-f + --p-trunc-len-r) -  min_merged_read_length >= 4 (4 is the absolute minimal)

#Choose paramters,such that the inequation is satisfied.

#How to select :

# choose location on forward (--p-trunc-len-f) and reservse (--p-trunc-len-r) reads,

#Find the positions in read qulaity which changes from green to orange in multiqc report

# starting from the end of the read, such that position is green zone in fastqc. 

# that is the quality from selected locations to the end of the read are less than 28 (are poor quality).

#For ITS:

#dada2 only merges reads, use exernal script to clean rreads

#use dedecated ITS CONFIG_DADA 

#Since the qiime2 pipeline is not fully automated I have grouped steps (rules in snakemake) into 8 subsections:

#1. manuel_import_qc

#2. Determine paramters for dada2 and quality check (manuel work), repeat dada2_all untill pass quality check

#3. dada2_all

#Deterimine input files for

#qiime_diversity_alpha_rarefaction (MAX_DEPTH)

#diversity core-metrics-phylogenetic (SAMPLING_DEPTH)

#Get these values from "results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_table.qzv"

#veiw AVS statsits to extract input vaules for 

#Find from interactive sample, and set MAX_DEPTH  to max vaule, and set SAMPLING_DEPTH to minimal values

#4. core_metrics_all

#5. Alpha diversity

#6. Beta diversity

#7. taxonomy all

#8. ancom all

#####START workflow##################

#usage: uncomment (delete '#') before command to run

#commands are located between consective  ####cmd##### lines

#hpc.sh contains a single line: bash snakemake_qiime.sh. It resolves runing issues on HPC of snakemake_qiime.sh due to variables defined at the top of this script.

#for non-HPC runs

#bash snakemake_qiime.sh

#for HPC runs

#hpc snakemake_qiime.sh

#rule manuel_import_qc

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_import/"$APLICON_TYPE"_per-sample-fastq-counts.tsv $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_manuel_import_qc.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_import/"$APLICON_TYPE"_per-sample-fastq-counts.tsv $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_manuel_import_qc.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_import/"$APLICON_TYPE"_per-sample-fastq-counts.tsv $CONFIG $CONFIG_DADA

####cmd#####

#2. Determine paramters for dada2 and quality check (manuel work), repeat dada2_all untill pass quality check

#1. qiime tools view  (optional)

####cmd#####

#qiime tools view "results/"$APLICON_TYPE"/qiime_import/"$APLICON_TYPE"_demux-paired-end.qzv"

####cmd#####


#3. dada2_all

# parmeters dada2 

# quality check

#all samples should have 50%  percentage of input non-chimeric.

#The minimal samples (replicates) for each experemint type (e.g, case and control) is 4.

#percentage of input non-chimeric is in denoising_stats.tsv

# e.g., #results/qiime_dada2_denoise_paired/16s_denoising_stats.tsv

#Change dada2 paramters, if samples fail quality check. 

#if this does not work STOP anaylsis

# connecting forward and reverse files

# makes a table, representative sequences, and statistics.

# rule dada2_all

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_table.qzv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_denoising_stats.tsv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_rep_seqs.fasta $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_dada2_all.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_table.qzv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_denoising_stats.tsv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_rep_seqs.fasta $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_dada2_all.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_table.qzv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_denoising_stats.tsv results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_rep_seqs.fasta $CONFIG $CONFIG_DADA

####cmd#####


#veiw AVS statsits to extract input vaules for 

#a) qiime_diversity_alpha_rarefaction:  MAX_DEPTH 

#b)diversity core-metrics-phylogenetic: SAMPLING_DEPTH

#Find from interactive sample, and set MAX_DEPTH  to max vaule, and set SAMPLING_DEPTH to minimal values

####cmd#####

#qiime tools view "results/"$APLICON_TYPE"/qiime_dada2_denoise_paired/"$APLICON_TYPE"_table.qzv"

####cmd#####


#4. core_metrics_all

#rule core_metrics_all

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/merged_out $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_core_metrics_all.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/merged_out $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_core_metrics_all.pdf 

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/merged_out $CONFIG $CONFIG_DADA


####cmd#####

#View core metrics results

####cmd#####

#unweighted_unifrac_emperor

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/unweighted_unifrac_emperor.qzv

#weighted_unifrac_emperor

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/weighted_unifrac_emperor.qzv

#jaccard_emperor

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/jaccard_emperor.qzv

#bray_curtis_emperor

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/bray_curtis_emperor.qzv

####cmd#####

#5 Alpha diverity

#alpha rarefaction (figures)

#rule qiime_diversity_alpha_rarefaction

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_alpha_rarefaction.qzv $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_alpha_rarefaction_figs.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_alpha_rarefaction.qzv $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_alpha_rarefaction_figs.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_alpha_rarefaction.qzv $CONFIG $CONFIG_DADA

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_alpha_rarefaction.qzv

####cmd#####

#rule diversity_alpha_group_significance_merege:

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_alpha_group_significance_merege.txt $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_diversity_alpha_group_significance.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_alpha_group_significance_merege.txt $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_diversity_alpha_group_significance.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_alpha_group_significance_merege.txt $CONFIG $CONFIG_DADA

#view reslts:

#faith_pd_vector:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/faith_pd_group_significance.qzv

#observed_features_vector:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/observed_features_vector_group_significance.qzv

#evenness_vector:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/evenness_vector_group_significance.qzv

#shannon_vector:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/shannon_vector_group_significance.qzv

####cmd#####

#6 Beta diverity

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_beta_group_significance_merege.txt $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_diversity_beta_group_significance.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_beta_group_significance_merege.txt $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_diversity_beta_group_significance.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/"$APLICON_TYPE"_diversity_beta_group_significance_merege.txt $CONFIG $CONFIG_DADA

#view reslts:

#unweighted_unifrac_distance_matrix:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/unweighted_unifrac_beta_group_significance.qzv

#weighted_unifrac_distance_matrix

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/weighted_unifrac_beta_group_significance.qzv

#jaccard_distance_matrix:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/jaccard_beta_group_significance.qzv

#bray_curtis_distance_matrix:

#qiime tools view results/"$APLICON_TYPE"/qiime_diversity/core_metrics_phylogenetic/bray_curtis_beta_group_significance.qzv

####cmd#####

#7. taxonomy all

# rule taxonomy all

####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxonomy.qzv results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxa_bar_plots.qzv  $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_taxonomy_all.txt

#snakemake --dag results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxonomy.qzv results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxa_bar_plots.qzv $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_taxonomy_all.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxonomy.qzv results/"$APLICON_TYPE"/qiime_diversity/"$APLICON_TYPE"_taxa_bar_plots.qzv $CONFIG $CONFIG_DADA

####cmd#####

#8. ANCOM,  all

#help on taxon names in ancom

#https://forum.qiime2.org/t/taxon-names-missing-in-ancom-results/17645/2


####cmd#####

#snakemake -np results/"$APLICON_TYPE"/qiime_ancom/"$APLICON_TYPE"_ancom_"$P_LEVEL"_"$CON_IN_COLUMNS"_combined.tsv $CONFIG $CONFIG_DADA > dry_run_"$APLICON_TYPE"_ancom_all.txt

#snakemake --dag  results/"$APLICON_TYPE"/qiime_ancom/"$APLICON_TYPE"_ancom_"$P_LEVEL"_"$CON_IN_COLUMNS"_combined.tsv $CONFIG $CONFIG_DADA | dot -Tpdf > "$APLICON_TYPE"_ancom_all.pdf

#snakemake --cores $CORES results/"$APLICON_TYPE"/qiime_ancom/"$APLICON_TYPE"_ancom_"$P_LEVEL"_"$CON_IN_COLUMNS"_combined.tsv $CONFIG $CONFIG_DADA

####cmd#####

#venn tables

####cmd#####


####cmd#####

##### END workflow##################
