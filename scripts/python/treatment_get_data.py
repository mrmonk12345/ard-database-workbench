
"""Provide treatment-scoped database queries as pandas DataFrames."""

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


# Data retrieval functions return records related to a treatment.
# Corresponding count functions return the number of matching records.


def get_treatment_element_assignments(treatment_id):
    """Return element assignments for a treatment."""
    query = f"""
    SELECT tea.*
    FROM treatment_element_assignments tea
    WHERE tea.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,))    
  
def get_treatment_element_assignments_count(treatment_id):
    """Return the number of element assignments for a treatment."""
    query = f"""
    SELECT COUNT(*) as count
    FROM treatment_element_assignments tea
    WHERE tea.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,)).iloc[0]['count']

def get_treatment_elements(treatment_id):
    """Return elements for a treatment."""
    query = f"""
    SELECT DISTINCT te.*
    FROM treatment_element_assignments tea
    JOIN treatment_elements te
      ON tea.treatment_element_id = te.treatment_element_id
    WHERE tea.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,))  

def get_treatment_elements_count(treatment_id):
    """Return the number of elements for a treatment."""
    query = f"""
    SELECT COUNT(DISTINCT te.treatment_element_id) as count
    FROM treatment_element_assignments tea
    JOIN treatment_elements te
      ON tea.treatment_element_id = te.treatment_element_id
    WHERE tea.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,)).iloc[0]['count'] 
  
def get_treatment_projects(treatment_id):
    """Return projects for a treatment."""
    query = f"""
    SELECT DISTINCT p.*
    FROM projects p
    JOIN samples s
      ON p.project_id = s.project_id
    WHERE s.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,))     
  
def get_treatment_projects_count(treatment_id):
    """Return the number of projects for a treatment."""
    query = f"""
    SELECT COUNT(DISTINCT p.project_id) as count
    FROM projects p
    JOIN samples s
      ON p.project_id = s.project_id
    WHERE s.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,)).iloc[0]['count'] 
  
  
def get_treatment_samples(treatment_id):
    """Return samples for a treatment."""
    query = f"""
    SELECT s.*
    FROM samples s
    WHERE s.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,))    

def get_treatment_samples_count(treatment_id):
    """Return the number of samples for a treatment."""
    query = f"""
    SELECT COUNT(*) as count
    FROM samples s
    WHERE s.treatment_id = ?
    """
    return run_query(query, params=(treatment_id,)).iloc[0]['count'] 

