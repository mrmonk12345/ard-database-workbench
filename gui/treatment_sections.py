"""Define treatment dashboard sections and their related actions."""

from scripts.python.treatment_get_data import (
    get_treatment_element_assignments,
    get_treatment_elements,
    get_treatment_samples,
    get_treatment_projects,

    get_treatment_element_assignments_count,
    get_treatment_elements_count,
    get_treatment_samples_count,
    get_treatment_projects_count,
)


def assignments_section(window):
    """Return the treatment-element assignments section configuration."""
    return {
        "title": "Treatment Assignments",

        "count": get_treatment_element_assignments_count(
            window.treatment_id
        ),

        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Treatment Assignments",
                    get_treatment_element_assignments(
                        window.treatment_id
                    ),
                    f"treatment_{window.treatment_id}_assignments.tsv"
                )
            ),

            (
                "Add",
                window.open_assignments_add
            ),
        ],
    }


def elements_section(window):
    """Return the treatment elements section configuration."""
    return {
        "title": "Treatment Elements",

        "count": get_treatment_elements_count(
            window.treatment_id
        ),

        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Treatment Elements",
                    get_treatment_elements(
                        window.treatment_id
                    ),
                    f"treatment_{window.treatment_id}_elements.tsv"
                )
            ),

            (
                "Add",
                window.open_elements_add
            ),
        ],
    }


def samples_section(window):
    """Return the treatment samples section configuration."""
    return {
        "title": "Samples",

        "count": get_treatment_samples_count(
            window.treatment_id
        ),

        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Samples",
                    get_treatment_samples(
                        window.treatment_id
                    ),
                    f"treatment_{window.treatment_id}_samples.tsv"
                )
            ),
        ],
    }


def projects_section(window):
    """Return the treatment projects section configuration."""
    return {
        "title": "Projects",

        "count": get_treatment_projects_count(
            window.treatment_id
        ),

        "buttons": [
            (
                "View",
                lambda: window.open_table(
                    "Projects",
                    get_treatment_projects(
                        window.treatment_id
                    ),
                    f"treatment_{window.treatment_id}_projects.tsv"
                )
            ),
        ],
    }
