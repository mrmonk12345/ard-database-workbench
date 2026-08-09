import argparse
import sqlite3
import pandas as pd

from config import DATABASE_PATH


def run_query(query, params=None):
    """Execute a SQL query and return the results as a DataFrame."""
    conn = sqlite3.connect(DATABASE_PATH)

    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df


def add_prefix(value, prefix):
    """Add a prefix to a value unless the value is the placeholder X."""
    return f"{prefix}{value}" if value != "X" else "X"


def update_labels(table_name, id_column, label_column, df):
    """Update label values in a database table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    query = f"""
        UPDATE {table_name}
        SET {label_column} = ?
        WHERE {id_column} = ?
          AND ({label_column} IS NULL OR {label_column} != ?)
    """
    
    cur.executemany(
        query,
        [
            [label, record_id, label]
            for label, record_id in df[[label_column, id_column]].values.tolist()
        ]
    )

    conn.commit()
    
    print(f"Updated {cur.rowcount} rows in {table_name}")
    print(
        f"Skipped {len(df) - cur.rowcount} rows in {table_name} "
        f"(label already up to date)"
    )


def refresh_all_labels(project_id):
    """Generate and save labels for all supported database entities."""

    update_labels(
        "libraries",
        "library_id",
        "label",
        make_libraries_labels(project_id).rename(
            columns={"library_label": "label"}
        )
    )

    update_labels(
        "sequencing_outputs",
        "sequencing_output_id",
        "label",
        make_sequencing_outputs_labels(project_id).rename(
            columns={"sequencing_output_label": "label"}
        )
    )

    update_labels(
        "analysis_units",
        "analysis_unit_id",
        "label",
        make_analysis_units_labels(project_id).rename(
            columns={"analysis_unit_label": "label"}
        )
    )


def make_libraries_labels(project_id):
    """Build labels for libraries from sample and amplicon metadata."""

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
    WHERE s.project_id = ?
    """

    df = run_query(query, (project_id,))

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


def make_sequencing_outputs_labels(project_id):
    """Build labels for sequencing outputs."""

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
    WHERE s.project_id = ?
    """

    df = run_query(query, (project_id,))

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


def make_analysis_units_labels(project_id):
    """Build labels for analysis units."""

    query = """
    SELECT
        au.analysis_unit_id,
        COALESCE(l.label, 'X') AS library_label,
        COALESCE(sr.sequencing_run_id, 'X') AS sequencing_run_id
    FROM analysis_units au
    LEFT JOIN libraries l
        ON au.library_id = l.library_id
    LEFT JOIN samples s
        ON l.sample_id = s.sample_id
    LEFT JOIN sequencing_runs sr
        ON au.sequencing_run_id = sr.sequencing_run_id
    WHERE s.project_id = ?
    """

    df = run_query(query, (project_id,))

    df["sequencing_run_id"] = df["sequencing_run_id"].apply(
        lambda x: add_prefix(x, "SR")
    )

    df["analysis_unit_label"] = (
        df["library_label"]
        + "_"
        + df["sequencing_run_id"]
    )

    return df[["analysis_unit_id", "analysis_unit_label"]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Refresh labels for a specific project."
    )
    parser.add_argument(
        "-p",
        "--project-id",
        type=int,
        required=True,
        help="Project ID",
    )

    args = parser.parse_args()

    refresh_all_labels(args.project_id)