# Database Tables

This document describes every table and view defined in `schema.sql`.

## Workflow tables

### `projects`
Stores study and research project metadata.

| Column | Description |
| --- | --- |
| `project_id` | Unique project identifier. |
| `label` | Human-readable project label. |
| `prjna` | NCBI BioProject accession. |
| `article_identifier` | Associated publication identifier. |
| `article_file_name` | Associated publication file name. |
| `notes` | Additional project notes. |
| `amplicon_type_id` | Default amplicon type. |

### `amplicon_types`
Defines genetic targets and primers used for amplicon sequencing.

| Column | Description |
| --- | --- |
| `amplicon_type_id` | Unique amplicon-type identifier. |
| `marker_gene` | Target marker gene. |
| `variable_region` | Target variable region. |
| `amplicon_length` | Expected amplicon length. |
| `f_name` | Forward primer name. |
| `f_sequence` | Forward primer sequence. |
| `f_length` | Forward primer length. |
| `r_name` | Reverse primer name. |
| `r_sequence` | Reverse primer sequence. |
| `r_length` | Reverse primer length. |

### `project_amplicon_types`
Associates projects with their amplicon types.

| Column | Description |
| --- | --- |
| `project_id` | Associated project. |
| `amplicon_type_id` | Associated amplicon type. |
| `role` | Amplicon-type role in the project. |

### `samples`
Stores biological sample metadata and experimental context.

| Column | Description |
| --- | --- |
| `sample_id` | Unique sample identifier. |
| `sample_name` | Original or local sample name. |
| `original_sample_label` | Label before standardization. |
| `label` | Standardized sample label. |
| `project_id` | Source project. |
| `soil_location_id` | Sample collection location. |
| `rootstock_id` | Associated rootstock. |
| `sampling_compartment_id` | Sample compartment. |
| `treatment_id` | Applied treatment. |
| `time_since_planting` | Time since planting. |
| `replicate_number` | Experimental replicate number. |
| `initial_health_status` | Initial health status. |
| `final_health_status` | Final health status. |
| `host_species` | Host organism species. |
| `scion_cultivar` | Associated scion cultivar. |
| `soil_texture` | Soil-texture classification. |
| `soil_type` | Soil-type classification. |
| `sampling_depth` | Sampling depth. |
| `experimental_setting` | Experimental setting. |
| `notes` | Additional sample notes. |

### `soil_locations`
Stores soil collection locations and related metadata.

| Column | Description |
| --- | --- |
| `soil_location_id` | Unique soil-location identifier. |
| `name` | Location name. |
| `label` | Short location label. |
| `country` | Country. |
| `city` | City or nearest locality. |
| `coordinates` | Geographic coordinates. |
| `project_id` | Associated project. |
| `soil_texture` | Soil-texture classification. |
| `soil_type` | Soil-type classification. |
| `notes` | Additional location notes. |

### `rootstocks`
Stores rootstock definitions.

| Column | Description |
| --- | --- |
| `rootstock_id` | Unique rootstock identifier. |
| `name` | Rootstock name. |
| `label` | Short rootstock label. |
| `rootstock_type` | Rootstock category. |
| `description` | Rootstock description. |

### `sampling_compartments`
Defines biological or physical sample compartments.

| Column | Description |
| --- | --- |
| `sampling_compartment_id` | Unique compartment identifier. |
| `name` | Compartment name. |
| `label` | Short compartment label. |
| `description` | Compartment description. |
| `project_id` | Defining or associated project. |

### `treatments`
Stores experimental treatments.

| Column | Description |
| --- | --- |
| `treatment_id` | Unique treatment identifier. |
| `name` | Treatment name. |
| `label` | Short treatment label. |
| `description` | Treatment description. |
| `project_id` | Project using the treatment. |
| `treatment_function` | Intended treatment function. |
| `notes` | Additional treatment notes. |

### `treatment_elements`
Defines components of experimental treatments.

| Column | Description |
| --- | --- |
| `treatment_element_id` | Unique element identifier. |
| `name` | Element name. |
| `category` | Broad element category. |
| `type` | Element type. |
| `subtype` | Element subtype. |
| `description` | Element description. |
| `notes` | Additional element notes. |

### `treatment_element_assignments`
Associates treatment elements with treatments.

| Column | Description |
| --- | --- |
| `treatment_id` | Treatment receiving the element. |
| `treatment_element_id` | Assigned treatment element. |
| `dose_value` | Applied dose. |
| `dose_unit` | Dose unit. |
| `duration_value` | Application duration. |
| `duration_unit` | Duration unit. |
| `application_method` | Application method. |
| `function` | Element function in the treatment. |
| `description` | Assignment description. |
| `notes` | Additional assignment notes. |

### `libraries`
Represents a prepared library linking a sample to an amplicon type.

| Column | Description |
| --- | --- |
| `library_id` | Unique library identifier. |
| `label` | Human-readable library label. |
| `sample_id` | Source sample. |
| `amplicon_type_id` | Library sequencing target. |
| `notes` | Additional library notes. |
| `srx` | NCBI SRA experiment accession. |
| `zzz_legacy_library_id` | Legacy library reference. |

### `sequencing_runs`
Records sequencing instrument runs.

| Column | Description |
| --- | --- |
| `sequencing_run_id` | Unique sequencing-run identifier. |
| `project_id` | Associated project. |
| `platform` | Sequencing platform or instrument. |
| `run_date` | Sequencing date. |
| `depth` | Run-level sequencing depth. |
| `read_type` | Read layout. |
| `notes` | Additional run notes. |

### `sequencing_outputs`
Stores raw sequencing files and their provenance.

| Column | Description |
| --- | --- |
| `sequencing_output_id` | Unique output identifier. |
| `label` | Human-readable output label. |
| `project_id` | Associated project. |
| `sample_id` | Represented sample. |
| `sequencing_run_id` | Source sequencing run. |
| `amplicon_type_id` | Represented amplicon type. |
| `srr` | NCBI SRA run accession. |
| `fastq1` | First or forward FASTQ path. |
| `fastq2` | Second or reverse FASTQ path. |
| `files_origin` | File origin. |
| `notes` | Additional output notes. |
| `zzz_legacy_library_id` | Legacy library reference. |

### `analysis_datasets`
Groups analysis units for processing.

| Column | Description |
| --- | --- |
| `analysis_dataset_id` | Unique dataset identifier. |
| `amplicon_type_id` | Dataset amplicon type. |
| `sequencing_run_id` | Dataset sequencing run. |
| `type` | Dataset category. |
| `notes` | Additional dataset notes. |

### `analysis_units`
Defines logical sample-level units used in analysis.

| Column | Description |
| --- | --- |
| `analysis_unit_id` | Unique analysis-unit identifier. |
| `analysis_unit_name` | Stable generated name. |
| `label` | Human-readable label. |
| `library_id` | Source library. |
| `sequencing_run_id` | Associated sequencing run. |
| `analysis_dataset_id` | Containing dataset. |

### `analysis_unit_files`
Tracks file preparation status and paths for analysis units.

| Column | Description |
| --- | --- |
| `analysis_unit_id` | Associated analysis unit. |
| `sequencing_output_id` | Source sequencing output. |
| `amplicon_separating_done` | Whether amplicon separation is complete. |
| `demultiplexing_done` | Whether demultiplexing is complete. |
| `gzip_done` | Whether gzip compression is complete. |
| `read1_path` | Prepared first-read path. |
| `read2_path` | Prepared second-read path. |

### `pipeline_definitions`
Defines pipeline, workflow, method, version, and parameter information.

| Column | Description |
| --- | --- |
| `pipeline_definition_id` | Unique definition identifier. |
| `pipeline_name` | Bioinformatic pipeline name. |
| `pipeline_version` | Pipeline version. |
| `workflow_name` | Workflow name. |
| `workflow_version` | Workflow version. |
| `method_name` | Analysis method name. |
| `method_version` | Analysis method version. |
| `parameters` | Pipeline parameters. |
| `notes` | Additional definition notes. |

### `pipeline_runs`
Tracks pipeline execution against an analysis dataset.

| Column | Description |
| --- | --- |
| `pipeline_run_id` | Unique pipeline-run identifier. |
| `pipeline_definition_id` | Definition used by the run. |
| `analysis_dataset_id` | Processed dataset. |
| `status` | Current or final status. |
| `trim_left_f` | Bases trimmed from forward reads. |
| `trim_left_r` | Bases trimmed from reverse reads. |
| `trunc_len_f` | Forward-read truncation length. |
| `trunc_len_r` | Reverse-read truncation length. |
| `p_min_overlap` | Minimum paired-read overlap. |
| `p_max_ee_f` | Maximum forward-read expected errors. |
| `p_max_ee_r` | Maximum reverse-read expected errors. |
| `sampling_depth` | Sampling or rarefaction depth. |
| `max_depth` | Maximum sequencing depth considered. |
| `processed_data_path` | Processed-results location. |
| `is_primary` | Whether this is the primary run. |
| `features_uploaded` | Whether feature sequences were uploaded. |
| `feature_counts_uploaded` | Whether feature counts were uploaded. |
| `taxonomy_uploaded` | Whether taxonomy was uploaded. |
| `notes` | Additional pipeline-run notes. |

### `features`
Stores sequence features generated by pipeline runs.

| Column | Description |
| --- | --- |
| `feature_id` | Unique feature identifier. |
| `pipeline_run_id` | Run that generated the feature. |
| `sequence` | Feature nucleotide sequence. |
| `sequence_hash` | Sequence hash or fingerprint. |
| `feature_type` | Sequence feature type. |

### `feature_counts`
Stores feature abundance in analysis units and pipeline runs.

| Column | Description |
| --- | --- |
| `feature_id` | Feature being counted. |
| `analysis_unit_id` | Unit in which the feature was observed. |
| `pipeline_run_id` | Run that produced the count. |
| `sample_id` | Sample corresponding to the unit. |
| `count` | Observed feature abundance. |

### `taxonomy`
Stores taxonomic assignments for sequence features.

| Column | Description |
| --- | --- |
| `feature_id` | Feature receiving the assignment. |
| `kingdom` | Assigned kingdom. |
| `phylum` | Assigned phylum. |
| `class` | Assigned class. |
| `order` | Assigned order. |
| `family` | Assigned family. |
| `genus` | Assigned genus. |
| `species` | Assigned species. |
| `confidence` | Assignment confidence. |
| `reference_db` | Reference database used. |
| `date_classified` | Classification date. |

## Supporting and import tables

### `directories`
Maps a name to a table and directory location.

| Column | Description |
| --- | --- |
| `name` | Directory mapping name. |
| `table_name` | Associated table name. |
| `directory` | Directory path or location. |

### `zzz_stg_samples_to_be_filled`
Staging table for sample metadata awaiting review or transfer. It contains the source fields `sample_name`, `Library Name`, `Sample Name`, `article_file_name`, `treatment_name`, `compartment_name`, `rootstock_name`, `sampling_health_status`, `final_health_status`, `location`, `previous_cultivation`, `time_since_planting`, `soil_texture`, `soil_type`, `sampling_depth`, and `experimental_setting`.

### `ref_SRA_run_info`
Stores metadata imported from NCBI SRA run records. Its columns are `Run`, `Assay Type`, `AvgSpotLen`, `Bases`, `BioProject`, `BioSample`, `BioSampleModel`, `Bytes`, `Center Name`, `Collection_Date`, `Consent`, `DATASTORE filetype`, `DATASTORE provider`, `DATASTORE region`, `Depth`, `elev`, `env_biome`, `env_feature`, `env_material`, `Experiment`, `geo_loc_name_country`, `geo_loc_name_country_continent`, `geo_loc_name`, `Instrument`, `lat_lon`, `Library Name`, `LibraryLayout`, `LibrarySelection`, `LibrarySource`, `Organism`, `Platform`, `ReleaseDate`, `create_date`, `version`, `Sample Name`, `SRA Study`, `filename (run)`, `filetype (run)`, `Host`, `isolation_source`, `platform (run)`, `samp_collect_device`, `samp_mat_process`, `samp_size`, `source_material_id`, `condition`, `multiplexing`, `pair`, `ref_biomaterial`, `marker`, `soil`, and `tmp`.

## Legacy and junction tables

### `zzz_library_amplicon_types`
Legacy library-to-amplicon-type junction table with `library_id`, `amplicon_type_id`, and `role`.

### `zzz_sequencing_run_libraries`
Legacy sequencing-run-to-library junction table with `sequencing_run_id`, `library_id`, `barcode`, and `notes`.

### `zzz_old_libaries_ncbi_srx`
Legacy library and NCBI SRA experiment table with `library_id`, `sample_id`, `amplicon_type_id`, `notes`, and `srx`. The table name preserves the original `libaries` spelling.

### `zzz_analysis_dataset_inputs`
Legacy analysis-dataset-to-analysis-unit junction table with `analysis_dataset_id` and `analysis_unit_id`.

### `zz_sequencing_outputs_amplicon_types`
Legacy sequencing-output-to-amplicon-type junction table with `sequencing_output_id` and `amplicon_type_id`.

### `sqlite_sequence`
SQLite-managed table tracking the last `AUTOINCREMENT` value, with `name` and `seq` columns.

## Views

### `NCBI_sample_run_info`
Combines sequencing outputs with sample IDs and matching NCBI SRA metadata.

### `vw_pipeline_run_summary`
Summarizes pipeline runs with project, amplicon type, sequencing-run, and pipeline-run information.

### `vw_pipeline_run_features_data`
Summarizes pipeline runs and includes the number of generated features plus upload-status flags.

## Workflow summary

- **Projects** describe the study.
- **Samples** describe biological material and experimental context.
- **Libraries** connect samples to sequencing targets.
- **Sequencing outputs** hold initial files and provenance.
- **Analysis units and datasets** define what will be processed.
- **Pipeline runs** record how processing was performed.
- **Features, feature counts, and taxonomy** store analysis results.
