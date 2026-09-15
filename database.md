# Database Overview

The database is organized around a clear and practical flow of information. It begins with biological and experimental context, then moves into sequencing and file handling, and finally reaches analysis and outputs.

## The main stages

1. **Project and sample metadata**
   Information about the study, samples, treatments, and experimental setup is stored first.

2. **Sequencing runs and raw files**
   The database records sequencing events and links them to the relevant files, such as FASTQ outputs.

3. **Libraries and analysis units**
   Samples and amplicon types are combined into libraries, and the database then defines analysis units for downstream processing.

4. **Pipeline runs and result tables**
   Once the data is prepared, the pipeline and its outputs are tracked in a structured way.

## Data organization layers

The schema is organized into several conceptual layers:

- **Biological and experimental metadata**: tables such as projects, samples, libraries, rootstocks, soil_locations, treatments, and sampling_compartments
- **Sequencing and ingestion metadata**: tables such as amplicon_types, project_amplicon_types, sequencing_runs, and sequencing_outputs. The amplicon tables define the biological targets used by each project.
- **Analysis and pipeline metadata**: tables such as analysis_units, analysis_datasets, and pipeline_runs
- **Result metadata**: tables such as feature_counts, features, and taxonomy
- **Reference and legacy tables**: tables such as ref_SRA_run_info, zzz_stg_samples_to_be_filled, and other zzz_* helper tables

## Design philosophy

The database keeps biological, experimental, technical, and analytical information connected so that results can be interpreted in the context in which the samples were collected and processed.

## Organizing sample metadata

A useful way to think about the metadata is by asking four questions:

- **When?** Temporal information such as dates, time since planting, or growth stage
- **What?** Experimental and biological context such as treatments, health status, or methods
- **Where?** Spatial and environmental information such as location, soil type, or climate-related traits
- **How?** Methods and technical details such as sampling compartment or sampling depth

This allows the database to store not only what was measured, but also the context in which the sample was collected and processed.

## From raw files to analysis units

The database separates raw data from processed analysis data so the same sequencing files can be reused in multiple workflows. This separation is important because raw sequencing files often arrive in a form that is not yet ready for analysis, while analysis units are defined in a more structured and consistent way. Sequencing outputs can therefore be recorded as they arrive before they are organized into analysis units for downstream processing.

### Sequencing outputs

Sequencing outputs represent the raw data layer. They can capture files exactly as they arrive from facilities and may not always include all the information needed for analysis. Attributes such as sequencing_run_id and amplicon_type_id may be nullable in practice, depending on how the files are recorded.

This flexibility allows the database to store files that are:

- Entire multiplexed runs
- Files pre-sorted by sample but containing multiple primer sets
- Fully demultiplexed target files

### Analysis units

Analysis units represent the structured target layer. Unlike raw files, they require a more complete and consistent form so downstream pipelines can process them reliably.

This design allows the system to bridge the gap between messy incoming data and the stricter demands of bioinformatics workflows.
