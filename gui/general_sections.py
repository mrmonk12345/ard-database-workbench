"""Define general-table dashboard sections and their related actions."""

from scripts.python.db_get_data import (
    get_projects,
    get_amplicon_types,
    get_project_amplicon_types,
    get_sequencing_runs,
    get_analysis_datasets,
    get_treatments,
    get_locations,
    get_rootstocks,
    get_sampling_compartments,
    get_pipeline_runs,
)


def projects_section(window):
    """Return the Projects section configuration."""
    return {
        "title": "Projects",
        "count": len(get_projects()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Projects",
                    get_projects(),
                    "projects.tsv",
                ),
            ),
        ],
    }


def amplicon_types_section(window):
    """Return the Amplicon Types section configuration."""
    return {
        "title": "Amplicon Types",
        "count": len(get_amplicon_types()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Amplicon Types",
                    get_amplicon_types(),
                    "amplicon_types.tsv",
                ),
            ),
        ],
    }


def project_amplicon_types_section(window):
    """Return the Project Amplicon Types section configuration."""
    return {
        "title": "Project Amplicon Types",
        "count": len(get_project_amplicon_types()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Project Amplicon Types",
                    get_project_amplicon_types(),
                    "project_amplicon_types.tsv",
                ),
            ),
        ],
    }


def sequencing_runs_section(window):
    """Return the Sequencing Runs section configuration."""
    return {
        "title": "Sequencing Runs",
        "count": len(get_sequencing_runs()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Sequencing Runs",
                    get_sequencing_runs(),
                    "sequencing_runs.tsv",
                ),
            ),
        ],
    }


def analysis_datasets_section(window):
    """Return the Analysis Datasets section configuration."""
    return {
        "title": "Analysis Datasets",
        "count": len(get_analysis_datasets()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Analysis Datasets",
                    get_analysis_datasets(),
                    "analysis_datasets.tsv",
                ),
            ),
        ],
    }


def treatments_section(window):
    """Return the Treatments section configuration."""
    return {
        "title": "Treatments",
        "count": len(get_treatments()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Treatments",
                    get_treatments(),
                    "treatments.tsv",
                ),
            ),
        ],
    }


def locations_section(window):
    """Return the Locations section configuration."""
    return {
        "title": "Locations",
        "count": len(get_locations()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Locations",
                    get_locations(),
                    "locations.tsv",
                ),
            ),
        ],
    }


def rootstocks_section(window):
    """Return the Rootstocks section configuration."""
    return {
        "title": "Rootstocks",
        "count": len(get_rootstocks()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Rootstocks",
                    get_rootstocks(),
                    "rootstocks.tsv",
                ),
            ),
        ],
    }


def sampling_compartments_section(window):
    """Return the Sampling Compartments section configuration."""
    return {
        "title": "Sampling Compartments",
        "count": len(get_sampling_compartments()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Sampling Compartments",
                    get_sampling_compartments(),
                    "sampling_compartments.tsv",
                ),
            ),
        ],
    }

def pipeline_runs_section(window):
    """Return the Pipeline Runs section configuration."""
    return {
        "title": "Pipeline Runs",
        "count": len(get_pipeline_runs()),
        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Pipeline Runs",
                    get_pipeline_runs(),
                    "pipeline_runs.tsv",
                ),
            ),
        ],
    }
