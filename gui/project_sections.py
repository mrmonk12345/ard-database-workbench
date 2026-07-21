from scripts.python.project_get_data import *


def samples_section(window):

    return {
        "title": "Samples",

        "count":
        get_project_samples_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Samples",
                    get_project_samples(
                        window.project_id
                    ),
                    f"project_{window.project_id}_samples.tsv"
                )
            ),

            (
                "Add",
                window.open_samples_add
            ),
        ]
    }


def outputs_section(window):

    return {

        "title":
        "Sequencing Outputs",

        "count":
        get_project_sequencing_outputs_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Sequencing Outputs",
                    get_project_sequencing_outputs(
                        window.project_id
                    ),
                    f"project_{window.project_id}_sequencing_outputs.tsv"
                )
            ),

            (
                "Add",
                window.open_outputs_add
            ),
        ]
    }


def libraries_section(window):

    return {

        "title":
        "Libraries",

        "count":
        get_project_libraries_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Libraries",
                    get_project_libraries(
                        window.project_id
                    ),
                    f"project_{window.project_id}_libraries.tsv"
                )
            ),

            (
                "Add",
                window.open_libraries_add
            ),
        ]
    }


def analysis_units_section(window):

    return {

        "title":
        "Analysis Units",

        "count":
        get_project_analysis_units_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Analysis Units",
                    get_project_analysis_units(
                        window.project_id
                    ),
                    f"project_{window.project_id}_analysis_units.tsv"
                )
            ),

            (
                "Add",
                window.open_analysis_units_add
            ),
        ]
    }


def analysis_unit_files_section(window):

    return {

        "title":
        "Analysis Unit Files",

        "count":
        get_project_analysis_unit_files_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Analysis Unit Files",
                    get_project_analysis_unit_files(
                        window.project_id
                    ),
                    f"project_{window.project_id}_analysis_unit_files.tsv"
                )
            ),
        ]
    }


def analysis_datasets_section(window):

    return {

        "title":
        "Analysis Datasets",

        "count":
        get_project_analysis_datasets_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Analysis Datasets",
                    get_project_analysis_datasets(
                        window.project_id
                    ),
                    f"project_{window.project_id}_analysis_datasets.tsv"
                )
            ),
        ]
    }


def analysis_dataset_inputs_section(window):

    return {

        "title":
        "Analysis Dataset Inputs",

        "count":
        get_project_analysis_dataset_inputs_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Analysis Dataset Inputs",
                    get_project_analysis_dataset_inputs(
                        window.project_id
                    ),
                    f"project_{window.project_id}_analysis_dataset_inputs.tsv"
                )
            ),
        ]
    }


def pipeline_runs_section(window):

    return {

        "title":
        "Pipeline Runs",

        "count":
        get_project_pipeline_runs_count(
            window.project_id
        ),

        "buttons": [

            (
                "View",
                lambda:
                window.open_table(
                    "Pipeline Runs",
                    get_project_pipeline_runs(
                        window.project_id
                    ),
                    f"project_{window.project_id}_pipeline_runs.tsv"
                )
            ),
        ]
    }