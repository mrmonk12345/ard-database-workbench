# Database Tables

This document describes every table defined in `schema.sql`, including workflow, supporting, staging, reference, junction, and legacy tables. The `NCBI_sample_run_info` view is documented at the end.

## Workflow tables

### `projects`
Stores study and research project metadata.

| Column | Description |
| --- | --- |
| `project_id` | Unique auto-incrementing project identifier. |
| `label` | Short human-readable project label. |
| `prjna` | NCBI BioProject accession, when available. |
| `article_identifier` | Identifier for the associated publication. |
| `article_file_name` | File name of the associated publication. |
| `notes` | Additional project notes. |
| `amplicon_type_id` | Default amplicon type for the project. |

### `amplicon_types`
Defines the genetic target and primers used for amplicon sequencing.

| Column | Description |
| --- | --- |
| `amplicon_type_id` | Unique amplicon-type identifier. |
| `marker_gene` | Target marker gene, such as 16S or ITS. |
| `variable_region` | Target variable region. |
| `amplicon_length` | Expected amplified-region length. |
| `f_name` | Forward primer name. |
| `f_sequence` | Forward primer nucleotide sequence. |
| `f_length` | Forward primer length. |
| `r_name` | Reverse primer name. |
| `r_sequence` | Reverse primer nucleotide sequence. |
| `r_length` | Reverse primer length. |

### `project_amplicon_types`
Associates projects with the amplicon types used in them.

| Column | Description |
| --- | --- |
| `project_id` | Associated project identifier. |
| `amplicon_type_id` | Associated amplicon-type identifier. |
| `role` | Purpose of the amplicon type in the project. |

### `samples`
Stores biological sample metadata and experimental context.

| Column | Description |
| --- | --- |
| `sample_id` | Unique auto-incrementing sample identifier. |
| `sample_name` | Original or local sample name. |
| `original_sample_label` | Sample label before standardization. |
| `label` | Standardized sample label. |
| `project_id` | Project from which the sample originated. |
| `location_id` | Sample collection location. |
| `rootstock_id` | Associated plant rootstock. |
| `sampling_compartment_id` | Biological or physical sampling compartment. |
| `treatment_id` | Applied experimental treatment. |
| `time_since_planting` | Time elapsed since planting at sampling. |
| `replicate_number` | Experimental replicate number. |
| `initial_health_status` | Health status at the start of observation. |
| `final_health_status` | Health status at the end of observation or sampling. |
| `host_species` | Host organism species. |
| `scion_cultivar` | Associated scion cultivar. |
| `soil_texture` | Physical soil-texture classification. |
| `soil_type` | Soil-type classification. |
| `sampling_depth` | Depth of sample collection. |
| `experimental_setting` | Experimental setting, such as field or greenhouse. |

### `locations`
Stores geographic locations associated with samples.

| Column | Description |
| --- | --- |
| `location_id` | Unique auto-incrementing location identifier. |
| `label` | Short location label. |
| `country` | Country containing the location. |
| `city` | City or nearest locality. |
| `coordinates` | Geographic coordinates. |

### `rootstocks`
Stores rootstock definitions used in experiments.

| Column | Description |
| --- | --- |
| `rootstock_id` | Unique auto-incrementing rootstock identifier. |
| `name` | Rootstock name. |
| `label` | Short rootstock label. |
| `rootstock_type` | Rootstock category or type. |
| `description` | Detailed rootstock description. |

### `sampling_compartments`
Defines biological or physical compartments used to classify sample origin.

| Column | Description |
| --- | --- |
| `sampling_compartment_id` | Unique auto-incrementing compartment identifier. |
| `name` | Compartment name. |
| `label` | Short compartment label. |
| `description` | Detailed compartment description. |
| `project_id` | Project defining or using the compartment. |

### `treatments`
Stores experimental treatments applied to projects or samples.

| Column | Description |
| --- | --- |
| `treatment_id` | Unique auto-incrementing treatment identifier. |
| `name` | Treatment name. |
| `label` | Short treatment label. |
| `description` | Treatment description. |
| `project_id` | Project in which the treatment is used. |
| `treatment_function` | Intended function or biological purpose. |

### `treatment_elements`
Defines components that can make up an experimental treatment.

| Column | Description |
| --- | --- |
| `treatment_element_id` | Unique auto-incrementing element identifier. |
| `name` | Treatment-element name. |
| `category` | Broad element category. |
| `type` | Element type. |
| `subtype` | More specific element subtype. |
| `notes` | Additional element notes. |

### `treatment_element_assignments`
Associates treatment elements with treatments and records their application.

| Column | Description |
| --- | --- |
| `treatment_id` | Treatment receiving the element. |
| `treatment_element_id` | Element included in the treatment. |
| `dose_value` | Numeric applied dose. |
| `dose_unit` | Unit of the dose. |
| `duration_value` | Numeric application duration. |
| `duration_unit` | Unit of the duration. |
| `application_method` | Method used to apply the element. |
| `function` | Element function within the treatment. |
| `notes` | Additional assignment notes. |

### `libraries`
Represents a prepared library linking a sample to an amplicon type.

| Column | Description |
| --- | --- |
| `library_id` | Unique auto-incrementing library identifier. |
| `label` | Human-readable library label. |
| `sample_id` | Sample used to prepare the library. |
| `amplicon_type_id` | Library sequencing target. |
| `notes` | Additional library notes. |
| `srx` | NCBI SRA experiment accession. |
| `zzz_legacy_library_id` | Legacy library reference. |

### `sequencing_runs`
Records a sequencing instrument run and its metadata.

| Column | Description |
| --- | --- |
| `sequencing_run_id` | Unique auto-incrementing run identifier. |
| `project_id` | Associated project. |
| `platform` | Sequencing platform or instrument. |
| `run_date` | Sequencing date. |
| `depth` | Run-level sequencing depth. |
| `read_type` | Read layout, such as single-end or paired-end. |
| `notes` | Additional run notes. |

### `sequencing_outputs`
Stores raw sequencing files and their provenance.

| Column | Description |
| --- | --- |
| `sequencing_output_id` | Unique auto-incrementing output identifier. |
| `label` | Human-readable output label. |
| `project_id` | Associated project. |
| `sample_id` | Sample represented in the output. |
| `sequencing_run_id` | Run that generated the output. |
| `amplicon_type_id` | Amplicon type represented in the output. |
| `srr` | NCBI SRA run accession. |
| `fastq1` | First or forward FASTQ path or file name. |
| `fastq2` | Second or reverse FASTQ path or file name. |
| `files_origin` | Origin or source of the files. |
| `notes` | Additional output notes. |
| `zzz_legacy_library_id` | Legacy library reference. |

### `analysis_datasets`
Groups analysis units for processing, usually by amplicon type and sequencing run.

| Column | Description |
| --- | --- |
| `analysis_dataset_id` | Unique auto-incrementing dataset identifier. |
| `amplicon_type_id` | Dataset amplicon type. |
| `sequencing_run_id` | Dataset sequencing run. |
| `type` | Dataset category, typically `base`. |
| `notes` | Additional dataset notes. |

### `analysis_units`
Defines logical sample-level units used in downstream analysis.

| Column | Description |
| --- | --- |
| `analysis_unit_id` | Unique auto-incrementing analysis-unit identifier. |
| `analysis_unit_name` | Stable generated analysis-unit name. |
| `label` | Human-readable analysis-unit label. |
| `library_id` | Source sequencing library. |
| `sequencing_run_id` | Sequencing run used by the unit. |
| `analysis_dataset_id` | Dataset containing the unit. |

### `analysis_unit_files`
Tracks file preparation status and paths for analysis units.

| Column | Description |
| --- | --- |
| `analysis_unit_id` | Analysis unit associated with the files. |
| `sequencing_output_id` | Source sequencing output. |
| `amplicon_separating_done` | Whether amplicon separation is complete. |
| `demultiplexing_done` | Whether demultiplexing is complete. |
| `gzip_done` | Whether gzip compression is complete. |
| `read1_path` | Prepared first-read file path. |
| `read2_path` | Prepared second-read file path. |

### `pipeline_definitions`
Defines pipeline, workflow, method, version, and parameter information.

| Column | Description |
| --- | --- |
| `pipeline_definition_id` | Unique auto-incrementing definition identifier. |
| `pipeline_name` | Bioinformatic pipeline name. |
| `pipeline_version` | Pipeline version. |
| `workflow_name` | Workflow name. |
| `workflow_version` | Workflow version. |
| `method_name` | Analysis method name. |
| `method_version` | Analysis method version. |
| `parameters` | Pipeline parameters or configuration. |

### `pipeline_runs`
Tracks pipeline execution against an analysis dataset.

| Column | Description |
| --- | --- |
| `pipeline_run_id` | Unique auto-incrementing run identifier. |
| `pipeline_definition_id` | Definition used for the run. |
| `analysis_dataset_id` | Dataset processed by the run. |
| `status` | Current or final execution status. |
| `trunc_len_f` | Forward-read truncation length. |
| `trunc_len_r` | Reverse-read truncation length. |
| `p_min_overlap` | Minimum paired-read overlap. |
| `p_max_ee_f` | Maximum expected forward-read errors. |
| `p_max_ee_r` | Maximum expected reverse-read errors. |
| `sampling_depth` | Sampling or rarefaction depth. |
| `max_depth` | Maximum sequencing depth considered. |
| `processed_data_path` | Location of processed results. |
| `is_primary` | Whether this is the primary run for the dataset. |
| `notes` | Additional pipeline-run notes. |

### `asvs`
Stores amplicon sequence variants generated by pipeline runs.

| Column | Description |
| --- | --- |
| `asv_id` | Unique ASV identifier. |
| `pipeline_run_id` | Run that generated the ASV. |
| `sequence` | ASV nucleotide sequence. |
| `sequence_hash` | Sequence hash or fingerprint. |

### `feature_counts`
Stores ASV abundance in analysis units and pipeline runs.

| Column | Description |
| --- | --- |
| `asv_id` | ASV being counted. |
| `analysis_unit_id` | Unit in which the ASV was observed. |
| `pipeline_run_id` | Run that produced the count. |
| `sample_id` | Sample corresponding to the unit. |
| `count` | Observed ASV abundance. |

### `taxonomy`
Stores taxonomic assignments for ASVs.

| Column | Description |
| --- | --- |
| `asv_id` | ASV receiving the assignment. |
| `kingdom` | Assigned kingdom. |
| `phylum` | Assigned phylum. |
| `class` | Assigned class. |
| `order` | Assigned order. |
| `family` | Assigned family. |
| `genus` | Assigned genus. |
| `species` | Assigned species. |
| `confidence` | Assignment confidence. |
| `reference_db` | Reference database used for classification. |
| `date_classified` | Classification date. |

## Supporting and import tables

### `directories`
Maps a name to a database table and directory location.

| Column | Description |
| --- | --- |
| `name` | Name of the directory mapping. |
| `table_name` | Associated table name. |
| `directory` | Directory path or location. |

### `zzz_stg_samples_to_be_filled`
Staging table for sample metadata awaiting review or transfer.

| Column | Description |
| --- | --- |
| `sample_name` | Source sample name. |
| `Library Name` | Source library name. |
| `Sample Name` | Source sample-name field. |
| `article_file_name` | Source article file name. |
| `treatment_name` | Source treatment name. |
| `compartment_name` | Source compartment name. |
| `rootstock_name` | Source rootstock name. |
| `sampling_health_status` | Health status at sampling. |
| `final_health_status` | Final health status. |
| `location` | Source location. |
| `previous_cultivation` | Previous cultivation information. |
| `time_since_planting` | Time since planting. |
| `soil_texture` | Source soil texture. |
| `soil_type` | Source soil type. |
| `sampling_depth` | Source sampling depth. |
| `experimental_setting` | Source experimental setting. |

### `ref_SRA_run_info`
Stores metadata imported from NCBI SRA run records.

| Column | Description |
| --- | --- |
| `Run` | Unique NCBI SRA run accession. |
| `Assay Type` | SRA assay type. |
| `AvgSpotLen` | Average spot or read length. |
| `Bases` | Number of bases reported by SRA. |
| `BioProject` | NCBI BioProject accession. |
| `BioSample` | NCBI BioSample accession. |
| `BioSampleModel` | NCBI BioSample model. |
| `Bytes` | Data size in bytes. |
| `Center Name` | Sequencing center name. |
| `Collection_Date` | Sample collection date. |
| `Consent` | Consent information. |
| `DATASTORE filetype` | Available data-store file type. |
| `DATASTORE provider` | Data-store provider. |
| `DATASTORE region` | Data-store region. |
| `Depth` | Reported sequencing depth. |
| `elev` | Collection-site elevation. |
| `env_biome` | Environmental biome. |
| `env_feature` | Environmental feature. |
| `env_material` | Environmental material. |
| `Experiment` | NCBI SRA experiment accession. |
| `geo_loc_name_country` | Geographic country. |
| `geo_loc_name_country_continent` | Geographic continent. |
| `geo_loc_name` | Reported geographic location. |
| `Instrument` | Sequencing instrument. |
| `lat_lon` | Latitude and longitude. |
| `Library Name` | SRA library name. |
| `LibraryLayout` | Library layout. |
| `LibrarySelection` | Library selection method. |
| `LibrarySource` | Library source category. |
| `Organism` | Associated organism. |
| `Platform` | Sequencing platform. |
| `ReleaseDate` | SRA public release date. |
| `create_date` | SRA record creation date. |
| `version` | Imported metadata version. |
| `Sample Name` | SRA sample name. |
| `SRA Study` | SRA study accession. |
| `filename (run)` | Run-level file name. |
| `filetype (run)` | Run-level file type. |
| `Host` | Host organism. |
| `isolation_source` | Material isolation source. |
| `platform (run)` | Run-level platform description. |
| `samp_collect_device` | Sample collection device. |
| `samp_mat_process` | Sample-material processing. |
| `samp_size` | Sample size. |
| `source_material_id` | Source-material identifier. |
| `condition` | Sample or experimental condition. |
| `multiplexing` | Multiplexing information. |
| `pair` | Read-pair information. |
| `ref_biomaterial` | Referenced biomaterial. |
| `marker` | Reported marker or target. |
| `soil` | Soil information. |
| `tmp` | Temporary or auxiliary imported value. |

### `zzz_library_amplicon_types`
Legacy junction table associating libraries with amplicon types.

| Column | Description |
| --- | --- |
| `library_id` | Legacy library identifier. |
| `amplicon_type_id` | Associated amplicon-type identifier. |
| `role` | Amplicon-type role for the library. |

### `zzz_sequencing_run_libraries`
Legacy junction table associating sequencing runs with libraries.

| Column | Description |
| --- | --- |
| `sequencing_run_id` | Sequencing run identifier. |
| `library_id` | Library identifier. |
| `barcode` | Library barcode in the run. |
| `notes` | Additional association notes. |

### `zzz_old_libaries_ncbi_srx`
Legacy table retaining library and NCBI SRA experiment information. The table name preserves the original `libaries` spelling.

| Column | Description |
| --- | --- |
| `library_id` | Legacy library identifier. |
| `sample_id` | Associated sample identifier. |
| `amplicon_type_id` | Associated amplicon-type identifier. |
| `notes` | Additional legacy notes. |
| `srx` | NCBI SRA experiment accession. |

### `zzz_analysis_dataset_inputs`
Legacy junction table associating analysis datasets with analysis units.

| Column | Description |
| --- | --- |
| `analysis_dataset_id` | Analysis dataset identifier. |
| `analysis_unit_id` | Analysis unit included in the dataset. |

### `zz_sequencing_outputs_amplicon_types`
Legacy junction table associating sequencing outputs with amplicon types.

| Column | Description |
| --- | --- |
| `sequencing_output_id` | Sequencing output identifier. |
| `amplicon_type_id` | Associated amplicon-type identifier. |

### `sqlite_sequence`
SQLite-managed table tracking the last value for `AUTOINCREMENT` tables.

| Column | Description |
| --- | --- |
| `name` | Table whose sequence is tracked. |
| `seq` | Most recently generated integer for that table. |

## Derived view

### `NCBI_sample_run_info`
Combines sequencing-output records with sample IDs and matching NCBI SRA metadata. It contains `sequencing_output_id`, `sample_id`, `project_id`, and `srr`, followed by the columns from `ref_SRA_run_info`.

## Workflow summary

- **Projects** describe the study.
- **Samples** describe biological material and experimental context.
- **Libraries** connect samples to sequencing targets.
- **Sequencing outputs** hold initial files and provenance.
- **Analysis units and datasets** define what will be processed.
- **Pipeline runs** record how processing was performed.
- **ASVs, feature counts, and taxonomy** store analysis results.
