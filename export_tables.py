import sqlite3
import pandas as pd
from pathlib import Path


from config import DATABASE_PATH, EXPORTED_RESULTS


# Connect to database
conn = sqlite3.connect(DATABASE_PATH)

print("1. Extracting Analysis Unit Metadata...")
au_metadata_query = """
SELECT DISTINCT
    au.analysis_unit_id,
    au.analysis_unit_name,
    au.label            AS au_label,
    au.library_id,
    au.sequencing_run_id,
    au.analysis_dataset_id,
    lib.sample_id,
    s.sample_name,
    p.label            AS project_label,
    tr.name            AS treatment_name,
    sc.name            AS compartment_name,
    r.name             AS rootstock_name,
    loc.name           AS soil_location_name,
    s.time_since_planting,
    s.initial_health_status,
    s.host_species,
    s.experimental_setting
    
FROM analysis_units au
LEFT JOIN libraries lib ON au.library_id = lib.library_id
LEFT JOIN samples s ON lib.sample_id = s.sample_id
LEFT JOIN projects p ON s.project_id = p.project_id
LEFT JOIN treatments tr ON s.treatment_id = tr.treatment_id
LEFT JOIN sampling_compartments sc ON s.sampling_compartment_id = sc.sampling_compartment_id
LEFT JOIN soil_locations loc ON s.soil_location_id = loc.soil_location_id
LEFT JOIN rootstocks r ON s.rootstock_id = r.rootstock_id
WHERE 1=1
    -- =========================================================
    -- ANALYSIS UNIT & METADATA FILTERS (Uncomment as needed)
    -- =========================================================
    AND p.project_id IN (15, 9, 7, 14)
    -- AND tr.name = 'Drought_Stress'
;
"""
df_au_metadata = pd.read_sql_query(au_metadata_query, conn).set_index("analysis_unit_id")

print("2. Extracting Sample Metadata...")
sample_metadata_query = """
SELECT DISTINCT
    s.sample_id,
    s.sample_name,
    s.original_sample_label,
    s.host_species,
    s.scion_cultivar,
    s.time_since_planting,
    s.replicate_number,
    s.initial_health_status,
    s.final_health_status,
    s.soil_texture,
    s.soil_type,
    s.sampling_depth,
    s.experimental_setting,
    p.project_id,
    p.label            AS project_label,
    p.prjna            AS project_prjna,
    loc.country        AS soil_location_country,
    loc.city           AS soil_location_city,
    tr.treatment_id,
    tr.name            AS treatment_name,
    sc.name            AS compartment_name,
    r.name             AS rootstock_name
FROM samples s
LEFT JOIN projects p ON s.project_id = p.project_id
LEFT JOIN soil_locations loc ON s.soil_location_id = loc.soil_location_id
LEFT JOIN treatments tr ON s.treatment_id = tr.treatment_id
LEFT JOIN sampling_compartments sc ON s.sampling_compartment_id = sc.sampling_compartment_id
LEFT JOIN rootstocks r ON s.rootstock_id = r.rootstock_id
WHERE 1=1
    -- =========================================================
    -- SAMPLE FILTERS (Uncomment as needed)
    -- =========================================================
    -- AND p.project_id IN (1, 2)
;
"""
df_sample_metadata = pd.read_sql_query(sample_metadata_query, conn).set_index("sample_id")

print("3. Extracting Taxonomy...")
taxonomy_query = """
SELECT DISTINCT
    feature_id, 
    kingdom, 
    phylum, 
    class, 
    "order", 
    family, 
    genus, 
    species, 
    confidence AS taxonomy_confidence, 
    reference_db AS taxonomy_ref_db
FROM taxonomy
WHERE 1=1
    -- =========================================================
    -- TAXONOMY FILTERS (Uncomment as needed)
    -- =========================================================
    AND reference_db = 'gtdb_r214'
;
"""
df_taxonomy = pd.read_sql_query(taxonomy_query, conn).set_index("feature_id")

print("4. Extracting Feature Counts...")
counts_query = """
SELECT 
    fc.feature_id, 
    fc.analysis_unit_id, 
    fc."count"
FROM feature_counts fc
;
"""
df_counts = pd.read_sql_query(counts_query, conn)

# Filter counts by active metadata and taxonomy selections


# -----------------------------------------------------------------------------
# 5. PIVOT & SAVE TSVS
# -----------------------------------------------------------------------------
print("Pivoting Count Matrix & Saving TSVs...")

# Ensure feature_id and analysis_unit_id types match across dataframes
df_counts["feature_id"] = df_counts["feature_id"].astype(str)
df_counts["analysis_unit_id"] = df_counts["analysis_unit_id"].astype(str)
df_taxonomy.index = df_taxonomy.index.astype(str)
df_au_metadata.index = df_au_metadata.index.astype(str)

count_matrix = df_counts.pivot(
    index="feature_id", 
    columns="analysis_unit_id", 
    values="count"
).fillna(0)

output_dir = Path(EXPORTED_RESULTS)
output_dir.mkdir(exist_ok=True)

# Save Count Matrix
count_matrix.to_csv(output_dir / "feature_count_matrix.tsv", sep="\t")

# Filter and save Taxonomy aligned to active features in matrix
active_features = count_matrix.index
df_taxonomy[df_taxonomy.index.isin(active_features)].to_csv(output_dir / "feature_taxonomy.tsv", sep="\t")

# Filter and save Analysis Unit Metadata aligned to active columns in matrix
active_aus = count_matrix.columns
df_au_metadata[df_au_metadata.index.isin(active_aus)].to_csv(output_dir / "analysis_unit_metadata.tsv", sep="\t")

# Filter and save Sample Metadata aligned to active sample_ids
if "sample_id" in df_au_metadata.columns:
    active_samples = df_au_metadata.loc[df_au_metadata.index.isin(active_aus), "sample_id"].dropna().astype(str).unique()
    df_sample_metadata.index = df_sample_metadata.index.astype(str)
    df_sample_metadata[df_sample_metadata.index.isin(active_samples)].to_csv(output_dir / "sample_metadata.tsv", sep="\t")

conn.close()

print("\nFinished successfully!")
print(f"Matrix shape: {count_matrix.shape[0]} features x {count_matrix.shape[1]} Analysis Units")
print("Files generated:")
print(" - feature_count_matrix.tsv       (Count matrix keyed by analysis_unit_id)")
print(" - feature_taxonomy.tsv           (Taxonomy table keyed by feature_id)")
print(" - analysis_unit_metadata.tsv (Analysis unit info + link to sample_id)")
print(" - sample_metadata.tsv        (Sample level metadata keyed by sample_id)")