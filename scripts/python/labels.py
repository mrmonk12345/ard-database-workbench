
import sqlite3
import pandas as pd


from config import DATABASE_PATH


def run_query(query, params=None):
    conn = sqlite3.connect(DATABASE_PATH)

    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df

def add_prefix(value, prefix):
    return f"{prefix}{value}" if value != "X" else "X"

def update_labels(table_name, id_column, label_column, df):
    """
    Update labels in a table.

    Parameters
    ----------
    table_name : str
        Table to update.
    id_column : str
        Primary key column.
    label_column : str
        Label column to update.
    df : DataFrame
        Must contain id_column and label_column.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    query = f"""
        UPDATE {table_name}
        SET {label_column} = ?
        WHERE {id_column} = ?
    """

    cur.executemany(
        query,
        df[[label_column, id_column]].values.tolist()
    )

    conn.commit()
    conn.close()

def refresh_all_labels():
    update_labels(
        "samples",
        "sample_id",
        "label",
        make_samples_labels().rename(columns={"sample_label": "label"})
    )

    update_labels(
        "libraries",
        "library_id",
        "label",
        make_libraries_labels().rename(columns={"library_label": "label"})
    )

    update_labels(
        "sequencing_outputs",
        "sequencing_output_id",
        "label",
        make_sequencing_outputs_labels().rename(
            columns={"sequencing_output_label": "label"}
        )
    )

    update_labels(
        "analysis_units",
        "analysis_unit_id",
        "label",
        make_analysis_units_labels().rename(
            columns={"analysis_unit_label": "label"}
        )
    )

def make_samples_labels():
    query = """
    SELECT
        s.sample_id,
        COALESCE(l.label, 'X') AS location,
        COALESCE(r.label, 'X') AS rootstock,
        COALESCE(sc.label, 'X') AS compartment,
        COALESCE(t.label, 'X') AS treatment,
        COALESCE(CAST(s.time_since_planting AS TEXT), 'X') AS time_since_planting,
        COALESCE(CAST(s.replicate_number AS TEXT), 'X') AS replicate
    FROM samples s
    LEFT JOIN locations l
        ON s.location_id = l.location_id
    LEFT JOIN rootstocks r
        ON s.rootstock_id = r.rootstock_id
    LEFT JOIN sampling_compartments sc
        ON s.sampling_compartment_id = sc.sampling_compartment_id
    LEFT JOIN treatments t
        ON s.treatment_id = t.treatment_id
    """
    
    df = run_query(query)


    df["replicate"] = df["replicate"].apply(
        lambda x: add_prefix(x, "R")
    )

    df["sample_label"] = (
        df["location"]
        + "_"
        + df["rootstock"]
        + "_"
        + df["compartment"]
        + "_"
        + df["treatment"]
        + "_"
        + df["time_since_planting"]
        + "_"
        + df["replicate"]
    )

    return df[["sample_id", "sample_label"]]

def make_libraries_labels():
    query = """
    SELECT
        l.library_id,
        COALESCE(s.label, 'X') AS sample_label,
        COALESCE(at.marker_gene, 'X') AS marker_gene,
        COALESCE(at.amplicon_type_id, 'X') AS amplicon_type_id
    FROM libraries l
    LEFT JOIN samples s
        ON l.sample_id = s.sample_id
    LEFT JOIN amplicon_types at
        ON l.amplicon_type_id = at.amplicon_type_id
    """
    
    df = run_query(query)

    df["amplicon_type_id"] = df["amplicon_type_id"].apply(
        lambda x: add_prefix(x, "AT")
    )

    df["library_label"] = (
        df["sample_label"]
        + "_"
        + df["marker_gene"]
        + "_"
        + df["amplicon_type_id"]
    )

    return df[["library_id", "library_label"]]

def make_sequencing_outputs_labels():
    query = """
    SELECT
        so.sequencing_output_id,
        COALESCE(s.label, 'X') AS sample_label,
        COALESCE(sr.sequencing_run_id, 'X') AS sequencing_run_id,
        COALESCE(at.marker_gene, 'X') AS marker_gene,
        COALESCE(at.amplicon_type_id, 'X') AS amplicon_type_id
    FROM sequencing_outputs so
    LEFT JOIN samples s
        ON so.sample_id = s.sample_id
    LEFT JOIN sequencing_runs sr
        ON so.sequencing_run_id = sr.sequencing_run_id
    LEFT JOIN amplicon_types at
        ON so.amplicon_type_id = at.amplicon_type_id
    """
    
    df = run_query(query)

    df["amplicon_type_id"] = df["amplicon_type_id"].apply(
        lambda x: add_prefix(x, "AT")
    )
    df["sequencing_run_id"] = df["sequencing_run_id"].apply(
        lambda x: add_prefix(x, "SR")
    )

    df["sequencing_output_label"] = (
        df["sample_label"]
        + "_"
        + df["marker_gene"]
        + "_"
        + df["amplicon_type_id"]
        + "_"
        + df["sequencing_run_id"]
    )

    return df[["sequencing_output_id", "sequencing_output_label"]]

def make_analysis_units_labels():
    query = """
    SELECT
        au.analysis_unit_id,
        COALESCE(l.label, 'X') AS library_label,
        COALESCE(sr.sequencing_run_id, 'X') AS sequencing_run_id
    FROM analysis_units au
    LEFT JOIN libraries l
        ON au.library_id = l.library_id
    LEFT JOIN sequencing_runs sr
        ON au.sequencing_run_id = sr.sequencing_run_id
    """
    
    df = run_query(query)

    df["sequencing_run_id"] = df["sequencing_run_id"].apply(
        lambda x: add_prefix(x, "SR")
    )

    df["analysis_unit_label"] = (
        df["library_label"]
        + "_"
        + df["sequencing_run_id"]
    )

    return df[["analysis_unit_id", "analysis_unit_label"]]