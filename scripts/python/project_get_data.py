
"""Provide project-scoped database queries as pandas DataFrames."""

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


# Data retrieval functions return all matching records for a project.
# Corresponding count functions return only the number of matching records.

def get_project_amplicon_types(project_id):
    """Return amplicon types associated with a project."""
    query = f"""
    SELECT at.*
    FROM amplicon_types at
    JOIN project_amplicon_types pat
      ON at.amplicon_type_id = pat.amplicon_type_id
    WHERE pat.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_amplicon_types_count(project_id):
    """Return the number of amplicon types associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM amplicon_types at
    JOIN project_amplicon_types pat
      ON at.amplicon_type_id = pat.amplicon_type_id
    WHERE pat.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_sequencing_runs(project_id):
    """Return sequencing runs associated with a project."""
    query = f"""
    SELECT *
    FROM sequencing_runs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_sequencing_runs_count(project_id):
    """Return the number of sequencing runs associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM sequencing_runs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_samples(project_id):
    """Return samples associated with a project."""
    query = f"""
    SELECT *
    FROM samples
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_samples_count(project_id):
    """Return the number of samples associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM samples
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_sequencing_outputs(project_id):
    """Return sequencing outputs associated with a project."""
    query = f"""
    SELECT *
    FROM sequencing_outputs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_sequencing_outputs_count(project_id):
    """Return the number of sequencing outputs associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM sequencing_outputs
    WHERE project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_libraries(project_id):
    """Return libraries associated with a project."""
    query = f"""
    SELECT l.*
    FROM libraries l
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_libraries_count(project_id):
    """Return the number of libraries associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM libraries l
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']


def get_project_analysis_units(project_id):
    """Return analysis units associated with a project."""
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
    """Return the number of analysis units associated with a project."""
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

def get_project_analysis_unit_files(project_id):
    """Return analysis unit files associated with a project."""
    query = f"""
    SELECT auf.*
    FROM analysis_unit_files auf
    JOIN analysis_units au
      ON auf.analysis_unit_id = au.analysis_unit_id
    JOIN libraries l
      ON au.library_id = l.library_id
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?    
    """
    return run_query(query, params=(project_id,))

def get_project_analysis_unit_files_count(project_id):
    """Return the number of analysis unit files associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM analysis_unit_files auf
    JOIN analysis_units au
      ON auf.analysis_unit_id = au.analysis_unit_id
    JOIN libraries l
      ON au.library_id = l.library_id
    JOIN samples s
      ON l.sample_id = s.sample_id
    WHERE s.project_id = ?    
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']
    
def get_project_analysis_datasets(project_id):
    """Return analysis datasets associated with a project."""
    query = f"""
    SELECT ad.*
    FROM analysis_datasets ad
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_analysis_datasets_count(project_id):
    """Return the number of analysis datasets associated with a project."""
    query = f"""
    SELECT COUNT(*) as count
    FROM analysis_datasets ad
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']

def get_project_analysis_dataset_inputs(project_id):
    """Return analysis dataset inputs associated with a project."""
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
    """Return the number of analysis dataset inputs associated with a project."""
    query = """
    SELECT COUNT(*) AS count
    FROM analysis_units au
    JOIN sequencing_runs sr
      ON au.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']

def get_project_pipeline_runs(project_id):
    """Return pipeline runs associated with a project."""
    query = """
    SELECT pr.*
    FROM pipeline_runs pr
    JOIN analysis_datasets ad
      ON pr.analysis_dataset_id = ad.analysis_dataset_id
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,))

def get_project_pipeline_runs_count(project_id):
    """Return the number of pipeline runs associated with a project."""
    query = """
    SELECT COUNT(*) AS count
    FROM pipeline_runs pr
    JOIN analysis_datasets ad
      ON pr.analysis_dataset_id = ad.analysis_dataset_id
    JOIN sequencing_runs sr
      ON ad.sequencing_run_id = sr.sequencing_run_id
    WHERE sr.project_id = ?
    """
    return run_query(query, params=(project_id,)).iloc[0]['count']
