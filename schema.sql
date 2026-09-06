CREATE TABLE IF NOT EXISTS "directories" (
	"name"	TEXT,
	"table_name"	TEXT,
	"directory"	TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "zzz_stg_samples_to_be_filled" (
	"sample_name"	TEXT,
	"Library Name"	TEXT,
	"Sample Name"	TEXT,
	"article_file_name"	TEXT,
	"treatment_name"	TEXT,
	"compartment_name"	TEXT,
	"rootstock_name"	TEXT,
	"sampling_health_status"	TEXT,
	"final_health_status"	TEXT,
	"location"	TEXT,
	"previous_cultivation"	TEXT,
	"time_since_planting"	TEXT,
	"soil_texture"	TEXT,
	"soil_type"	TEXT,
	"sampling_depth"	TEXT,
	"experimental_setting"	TEXT
);
CREATE TABLE IF NOT EXISTS "zzz_library_amplicon_types" (
	"library_id"	INTEGER,
	"amplicon_type_id"	INTEGER,
	"role"	TEXT,
	PRIMARY KEY("library_id","amplicon_type_id")
);
CREATE TABLE IF NOT EXISTS "zzz_sequencing_run_libraries" (
	"sequencing_run_id"	INTEGER,
	"library_id"	INTEGER,
	"barcode"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("sequencing_run_id","library_id")
);
CREATE TABLE IF NOT EXISTS "zzz_old_libaries_ncbi_srx" (
	"library_id"	INTEGER,
	"sample_id"	INTEGER,
	"amplicon_type_id"	TEXT,
	"notes"	TEXT,
	"srx"	TEXT
);
CREATE TABLE IF NOT EXISTS "analysis_unit_files" (
	"analysis_unit_id"	INTEGER NOT NULL,
	"sequencing_output_id"	INTEGER,
	"amplicon_separating_done"	BOOLEAN,
	"demultiplexing_done"	BOOLEAN,
	"gzip_done"	BOOLEAN,
	"read1_path"	TEXT,
	"read2_path"	TEXT,
	PRIMARY KEY("analysis_unit_id" AUTOINCREMENT),
	FOREIGN KEY("analysis_unit_id") REFERENCES "analysis_units"("analysis_unit_id"),
	FOREIGN KEY("sequencing_output_id") REFERENCES "sequencing_outputs"("sequencing_output_id")
);
CREATE TABLE IF NOT EXISTS "sequencing_runs" (
	"sequencing_run_id"	INTEGER NOT NULL,
	"project_id"	INTEGER NOT NULL,
	"platform"	TEXT,
	"run_date"	TEXT,
	"depth"	TEXT,
	"read_type"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("sequencing_run_id" AUTOINCREMENT),
	FOREIGN KEY("project_id") REFERENCES "projects"("project_id")
);
CREATE TABLE IF NOT EXISTS "ref_SRA_run_info" (
	"Run"	TEXT NOT NULL UNIQUE,
	"Assay Type"	TEXT,
	"AvgSpotLen"	INTEGER,
	"Bases"	INTEGER,
	"BioProject"	TEXT,
	"BioSample"	TEXT,
	"BioSampleModel"	TEXT,
	"Bytes"	INTEGER,
	"Center Name"	TEXT,
	"Collection_Date"	TEXT,
	"Consent"	TEXT,
	"DATASTORE filetype"	TEXT,
	"DATASTORE provider"	TEXT,
	"DATASTORE region"	TEXT,
	"Depth"	TEXT,
	"elev"	REAL,
	"env_biome"	TEXT,
	"env_feature"	TEXT,
	"env_material"	TEXT,
	"Experiment"	TEXT,
	"geo_loc_name_country"	TEXT,
	"geo_loc_name_country_continent"	TEXT,
	"geo_loc_name"	TEXT,
	"Instrument"	TEXT,
	"lat_lon"	TEXT,
	"Library Name"	TEXT,
	"LibraryLayout"	TEXT,
	"LibrarySelection"	TEXT,
	"LibrarySource"	TEXT,
	"Organism"	TEXT,
	"Platform"	TEXT,
	"ReleaseDate"	TEXT,
	"create_date"	TEXT,
	"version"	REAL,
	"Sample Name"	TEXT,
	"SRA Study"	TEXT,
	"filename (run)"	TEXT,
	"filetype (run)"	TEXT,
	"Host"	TEXT,
	"isolation_source"	TEXT,
	"platform (run)"	TEXT,
	"samp_collect_device"	TEXT,
	"samp_mat_process"	TEXT,
	"samp_size"	TEXT,
	"source_material_id"	TEXT,
	"condition"	TEXT,
	"multiplexing"	TEXT,
	"pair"	TEXT,
	"ref_biomaterial"	TEXT,
	"marker"	TEXT,
	"soil"	TEXT,
	"tmp"	TEXT,
	PRIMARY KEY("Run")
);
CREATE TABLE IF NOT EXISTS "amplicon_types" (
	"amplicon_type_id"	INTEGER NOT NULL UNIQUE,
	"marker_gene"	TEXT,
	"variable_region"	TEXT,
	"amplicon_length"	INTEGER,
	"f_name"	TEXT,
	"f_sequence"	TEXT,
	"f_length"	INTEGER,
	"r_name"	TEXT,
	"r_sequence"	TEXT,
	"r_length"	INTEGER,
	PRIMARY KEY("amplicon_type_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "zzz_analysis_dataset_inputs" (
	"analysis_dataset_id"	INTEGER NOT NULL,
	"analysis_unit_id"	INTEGER NOT NULL,
	PRIMARY KEY("analysis_dataset_id","analysis_unit_id")
);
CREATE TABLE IF NOT EXISTS "zz_sequencing_outputs_amplicon_types" (
	"sequencing_output_id"	INTEGER NOT NULL,
	"amplicon_type_id"	INTEGER NOT NULL,
	PRIMARY KEY("sequencing_output_id","amplicon_type_id")
);
CREATE TABLE IF NOT EXISTS "analysis_units" (
	"analysis_unit_id"	INTEGER NOT NULL,
	"analysis_unit_name"	TEXT,
	"label"	TEXT,
	"library_id"	INTEGER NOT NULL,
	"sequencing_run_id"	INTEGER NOT NULL,
	"analysis_dataset_id"	INTEGER,
	PRIMARY KEY("analysis_unit_id" AUTOINCREMENT),
	CONSTRAINT "analysis_unit_identity" UNIQUE("library_id","sequencing_run_id"),
	FOREIGN KEY("analysis_dataset_id") REFERENCES "analysis_datasets"("analysis_dataset_id"),
	FOREIGN KEY("library_id") REFERENCES "libraries"("library_id"),
	FOREIGN KEY("sequencing_run_id") REFERENCES "sequencing_runs"("sequencing_run_id")
);
CREATE TABLE IF NOT EXISTS "libraries" (
	"library_id"	INTEGER NOT NULL,
	"label"	TEXT,
	"sample_id"	INTEGER NOT NULL,
	"amplicon_type_id"	INTEGER NOT NULL,
	"notes"	TEXT,
	"srx"	TEXT,
	"zzz_legacy_library_id"	INTEGER,
	PRIMARY KEY("library_id" AUTOINCREMENT),
	CONSTRAINT "library_identity" UNIQUE("sample_id","amplicon_type_id"),
	FOREIGN KEY("amplicon_type_id") REFERENCES "amplicon_types"("amplicon_type_id"),
	CONSTRAINT "fk_sra_runs_sample_id" FOREIGN KEY("sample_id") REFERENCES "samples"("sample_id")
);
CREATE TABLE IF NOT EXISTS "rootstocks" (
	"rootstock_id"	INTEGER,
	"name"	TEXT,
	"label"	INTEGER,
	"rootstock_type"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("rootstock_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sampling_compartments" (
	"sampling_compartment_id"	INTEGER,
	"name"	TEXT,
	"label"	INTEGER,
	"description"	TEXT,
	"project_id"	INTEGER,
	PRIMARY KEY("sampling_compartment_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "projects" (
	"project_id"	INTEGER NOT NULL UNIQUE,
	"label"	TEXT,
	"prjna"	TEXT,
	"article_identifier"	TEXT,
	"article_file_name"	TEXT,
	"notes"	TEXT,
	"amplicon_type_id"	TEXT,
	PRIMARY KEY("project_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "project_amplicon_types" (
	"project_id"	INTEGER,
	"amplicon_type_id"	TEXT,
	"role"	TEXT,
	FOREIGN KEY("amplicon_type_id") REFERENCES "amplicon_types"("amplicon_type_id"),
	FOREIGN KEY("project_id") REFERENCES "projects"("project_id")
);
CREATE TABLE IF NOT EXISTS "analysis_datasets" (
	"analysis_dataset_id"	INTEGER NOT NULL,
	"amplicon_type_id"	INTEGER NOT NULL,
	"sequencing_run_id"	INTEGER NOT NULL,
	"type"	TEXT,
	"notes"	INTEGER,
	PRIMARY KEY("analysis_dataset_id" AUTOINCREMENT),
	FOREIGN KEY("amplicon_type_id") REFERENCES "amplicon_types"("amplicon_type_id"),
	FOREIGN KEY("sequencing_run_id") REFERENCES "sequencing_runs"("sequencing_run_id")
);
CREATE TABLE IF NOT EXISTS "sequencing_outputs" (
	"sequencing_output_id"	INTEGER NOT NULL,
	"label"	TEXT,
	"project_id"	INTEGER,
	"sample_id"	INTEGER,
	"sequencing_run_id"	INTEGER,
	"amplicon_type_id"	INTEGER,
	"srr"	TEXT,
	"fastq1"	TEXT,
	"fastq2"	TEXT,
	"files_origin"	TEXT,
	"notes"	TEXT,
	"zzz_legacy_library_id"	INTEGER,
	PRIMARY KEY("sequencing_output_id" AUTOINCREMENT),
	FOREIGN KEY("amplicon_type_id") REFERENCES "amplicon_types"("amplicon_type_id"),
	FOREIGN KEY("sample_id") REFERENCES "samples"("sample_id"),
	FOREIGN KEY("sequencing_run_id") REFERENCES "sequencing_runs"("sequencing_run_id")
);
CREATE TABLE IF NOT EXISTS "samples" (
	"sample_id"	INTEGER NOT NULL UNIQUE,
	"sample_name"	TEXT,
	"original_sample_label"	TEXT,
	"label"	TEXT,
	"project_id"	INTEGER,
	"soil_location_id"	INTEGER,
	"rootstock_id"	INTEGER,
	"sampling_compartment_id"	INTEGER,
	"treatment_id"	INTEGER,
	"time_since_planting"	TEXT,
	"replicate_number"	INTEGER,
	"initial_health_status"	TEXT,
	"final_health_status"	TEXT,
	"host_species"	TEXT,
	"scion_cultivar"	TEXT,
	"soil_texture"	TEXT,
	"soil_type"	TEXT,
	"sampling_depth"	TEXT,
	"experimental_setting"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("sample_id" AUTOINCREMENT),
	CONSTRAINT "fk_samples_project_id" FOREIGN KEY("project_id") REFERENCES "projects"("project_id"),
	CONSTRAINT "fk_samples_rootstock_id" FOREIGN KEY("rootstock_id") REFERENCES "rootstocks"("rootstock_id"),
	FOREIGN KEY("sampling_compartment_id") REFERENCES "sampling_compartments"("sampling_compartment_id"),
	FOREIGN KEY("soil_location_id") REFERENCES "soil_locations"("soil_location_id"),
	CONSTRAINT "fk_samples_treatment_id" FOREIGN KEY("treatment_id") REFERENCES "treatments"("treatment_id")
);
CREATE VIEW NCBI_sample_run_info AS
SELECT
	so.sequencing_output_id,
    s.sample_id,
	so.project_id,
    so.srr,
    ref.*
FROM sequencing_outputs so
LEFT JOIN samples s
    ON s.sample_id = so.sample_id
LEFT JOIN ref_SRA_run_info ref
    ON so.srr = ref.Run
/* NCBI_sample_run_info(sequencing_output_id,sample_id,project_id,srr,Run,"Assay Type",AvgSpotLen,Bases,BioProject,BioSample,BioSampleModel,Bytes,"Center Name",Collection_Date,Consent,"DATASTORE filetype","DATASTORE provider","DATASTORE region",Depth,elev,env_biome,env_feature,env_material,Experiment,geo_loc_name_country,geo_loc_name_country_continent,geo_loc_name,Instrument,lat_lon,"Library Name",LibraryLayout,LibrarySelection,LibrarySource,Organism,Platform,ReleaseDate,create_date,version,"Sample Name","SRA Study","filename (run)","filetype (run)",Host,isolation_source,"platform (run)",samp_collect_device,samp_mat_process,samp_size,source_material_id,condition,multiplexing,pair,ref_biomaterial,marker,soil,tmp) */;
CREATE TABLE IF NOT EXISTS "soil_locations" (
	"soil_location_id"	INTEGER,
	"name"	TEXT,
	"label"	TEXT,
	"country"	TEXT,
	"city"	TEXT,
	"coordinates"	TEXT,
	"project_id"	INTEGER,
	"soil_texture"	TEXT,
	"soil_type"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("soil_location_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "features" (
	"feature_id"	INTEGER NOT NULL,
	"pipeline_run_id"	INTEGER,
	"sequence"	TEXT,
	"sequence_hash"	TEXT,
	"feature_type"	TEXT,
	PRIMARY KEY("feature_id" AUTOINCREMENT),
	UNIQUE("pipeline_run_id","sequence"),
	FOREIGN KEY("pipeline_run_id") REFERENCES "pipeline_runs"("pipeline_run_id")
);
CREATE TABLE IF NOT EXISTS "feature_counts" (
	"feature_id"	INTEGER NOT NULL,
	"analysis_unit_id"	INTEGER NOT NULL,
	"pipeline_run_id"	INTEGER,
	"sample_id"	INTEGER,
	"count"	INTEGER,
	CONSTRAINT "abunance_pk" PRIMARY KEY("feature_id","analysis_unit_id"),
	FOREIGN KEY("analysis_unit_id") REFERENCES "analysis_units"("analysis_unit_id"),
	CONSTRAINT "fk_abundance_asv_id" FOREIGN KEY("feature_id") REFERENCES "features"("feature_id"),
	FOREIGN KEY("pipeline_run_id") REFERENCES "pipeline_runs"("pipeline_run_id")
);
CREATE TABLE IF NOT EXISTS "pipeline_runs" (
	"pipeline_run_id"	INTEGER,
	"pipeline_definition_id"	INTEGER,
	"analysis_dataset_id"	INTEGER,
	"status"	TEXT,
	"trim_left_f"	INTEGER,
	"trim_left_r"	INTEGER,
	"trunc_len_f"	INTEGER,
	"trunc_len_r"	INTEGER,
	"p_min_overlap"	INTEGER,
	"p_max_ee_f"	INTEGER,
	"p_max_ee_r"	INTEGER,
	"sampling_depth"	INTEGER,
	"max_depth"	INTEGER,
	"processed_data_path"	TEXT,
	"is_primary"	INTEGER,
	"features_uploaded"	INTEGER,
	"feature_counts_uploaded"	INTEGER,
	"taxonomy_uploaded"	INTEGER,
	"notes"	TEXT,
	PRIMARY KEY("pipeline_run_id" AUTOINCREMENT),
	FOREIGN KEY("analysis_dataset_id") REFERENCES "analysis_datasets"("analysis_dataset_id"),
	FOREIGN KEY("pipeline_definition_id") REFERENCES "pipeline_definitions"("pipeline_definition_id")
);
CREATE VIEW vw_pipeline_run_summary AS
SELECT
    pr.pipeline_run_id,
    p.project_id,
    p.label AS project_label,
	p.article_identifier AS project_article,
    at.marker_gene,
    sr.notes AS sequencing_run_notes
FROM pipeline_runs pr
JOIN analysis_datasets ad
    ON ad.analysis_dataset_id = pr.analysis_dataset_id
JOIN sequencing_runs sr
    ON sr.sequencing_run_id = ad.sequencing_run_id
JOIN projects p
    ON p.project_id = sr.project_id
JOIN amplicon_types at
    ON at.amplicon_type_id = ad.amplicon_type_id
/* vw_pipeline_run_summary(pipeline_run_id,project_id,project_label,project_article,marker_gene,sequencing_run_notes) */;
CREATE TABLE IF NOT EXISTS "pipeline_definitions" (
	"pipeline_definition_id"	INTEGER,
	"pipeline_name"	TEXT,
	"pipeline_version"	TEXT,
	"workflow_name"	TEXT,
	"workflow_version"	INTEGER,
	"method_name"	INTEGER,
	"method_version"	INTEGER,
	"parameters"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("pipeline_definition_id" AUTOINCREMENT)
);
CREATE VIEW vw_pipeline_run_features_data AS
SELECT
    pr.pipeline_run_id,
    pr.pipeline_definition_id,
    pr.analysis_dataset_id,
    p.project_id,
    p.label AS project_label,
    p.article_identifier AS project_article,
    at.marker_gene,
    sr.notes AS sequencing_run_notes,
    pr.notes AS pipeline_run_notes,
    pr.is_primary,
    pr.features_uploaded,
    pr.feature_counts_uploaded,
    pr.taxonomy_uploaded,
    COALESCE(fc.features, 0) AS features
FROM pipeline_runs pr
JOIN analysis_datasets ad
    ON ad.analysis_dataset_id = pr.analysis_dataset_id
JOIN sequencing_runs sr
    ON sr.sequencing_run_id = ad.sequencing_run_id
JOIN projects p
    ON p.project_id = sr.project_id
JOIN amplicon_types at
    ON at.amplicon_type_id = ad.amplicon_type_id
LEFT JOIN (
    SELECT
        pipeline_run_id,
        COUNT(*) AS features
    FROM features
    GROUP BY pipeline_run_id
) fc
    ON fc.pipeline_run_id = pr.pipeline_run_id
/* vw_pipeline_run_features_data(pipeline_run_id,pipeline_definition_id,analysis_dataset_id,project_id,project_label,project_article,marker_gene,sequencing_run_notes,pipeline_run_notes,is_primary,features_uploaded,feature_counts_uploaded,taxonomy_uploaded,features) */;
CREATE TABLE IF NOT EXISTS "treatments" (
	"treatment_id"	INTEGER,
	"name"	TEXT,
	"label"	TEXT,
	"description"	TEXT,
	"project_id"	INTEGER,
	"treatment_function"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("treatment_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "treatment_elements" (
	"treatment_element_id"	INTEGER,
	"name"	TEXT,
	"category"	TEXT,
	"type"	TEXT,
	"subtype"	TEXT,
	"description"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("treatment_element_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "treatment_element_assignments" (
	"treatment_id"	INTEGER,
	"treatment_element_id"	INTEGER,
	"dose_value"	NUMERIC,
	"dose_unit"	TEXT,
	"duration_value"	NUMERIC,
	"duration_unit"	TEXT,
	"application_method"	TEXT,
	"function"	TEXT,
	"description"	TEXT,
	"notes"	TEXT,
	PRIMARY KEY("treatment_id","treatment_element_id"),
	FOREIGN KEY("treatment_element_id") REFERENCES "treatment_elements"("treatment_element_id"),
	FOREIGN KEY("treatment_id") REFERENCES "treatments"("treatment_id")
);
CREATE TABLE IF NOT EXISTS "taxonomy" (
	"feature_id"	TEXT,
	"kingdom"	TEXT,
	"phylum"	TEXT,
	"class"	TEXT,
	"order"	TEXT,
	"family"	TEXT,
	"genus"	TEXT,
	"species"	TEXT,
	"confidence"	TEXT,
	"reference_db"	TEXT,
	"date_classified"	TEXT,
	UNIQUE("feature_id","reference_db"),
	CONSTRAINT "fk_taxonomy_asv_id" FOREIGN KEY("feature_id") REFERENCES "features"("feature_id")
);
