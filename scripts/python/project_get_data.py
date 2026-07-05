
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


# ✅ ---- DATA TABLES ----

def get_project_amplicon_types(project_id):
    query = f"""
    SELECT at.*
    FROM amplicon_types at
    JOIN project_amplicon_types pat
      ON at.amplicon_type_id = pat.amplicon_type_id
    WHERE pat.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_amplicon_types_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM amplicon_types at
    JOIN project_amplicon_types pat
      ON at.amplicon_type_id = pat.amplicon_type_id
    WHERE pat.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_sequencing_runs(project_id):
    query = f"""
    SELECT *
    FROM sequencing_runs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_sequencing_runs_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM sequencing_runs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_samples(project_id):
    query = f"""
    SELECT *
    FROM samples
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_samples_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM samples
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_sequencing_outputs(project_id):
    query = f"""
    SELECT *
    FROM sequencing_outputs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_sequencing_outputs_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM sequencing_outputs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_libraries(project_id):
    query = f"""
    SELECT l.*
    FROM libraries l
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_libraries_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM libraries l
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_analysis_units(project_id):
    query = f"""
    SELECT au.*
    FROM analysis_units au
    JOIN libraries l
      ON au.library_id = l.library_id
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_analysis_units_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM analysis_units au
    JOIN libraries l
      ON au.library_id = l.library_id
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']

def get_project_analysis_datasets(project_id):
    query = f"""
    SELECT ad.*
    FROM analysis_datasets ad
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_analysis_datasets_count(project_id):
    query = f"""
    SELECT COUNT(*) as count
    FROM analysis_datasets ad
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']

def get_project_analysis_dataset_inputs(project_id):
    query = """
    SELECT
      au.analysis_dataset_id, 
      au.analysis_unit_id
    FROM analysis_units au
    JOIN sequencing_runs sr
      ON au.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_analysis_dataset_inputs_count(project_id):
    query = """
    SELECT COUNT(*) AS count
    FROM analysis_units au
    JOIN sequencing_runs sr
      ON au.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']