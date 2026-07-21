#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path

from config import DATABASE_PATH

PALETTE = [
    "#377eb8",
    "#e41a1c",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#a65628",
    "#f781bf",
    "#66c2a5",
    "#fc8d62",
    "#8da0cb",
    "#e78ac3",
    "#a6d854",
]


def get_color(value, color_map):
    if value not in color_map:
        color_map[value] = PALETTE[
            len(color_map) % len(PALETTE)
        ]
    return color_map[value]


def add_node(nodes, node_id, label):
    nodes.add(f'{node_id}["{label}"]')


def add_edge(edges, source, target):
    edges.add(f"{source} --> {target}")


def add_missing_node(nodes, classes, node_id, label):
    add_node(nodes, node_id, label)
    classes.append(f"class {node_id} missing")


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python graph_project.py <project_id>")
        return

    project_id = int(sys.argv[1])

    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    nodes = set()
    edges = set()
    classes = []

    dataset_colors = {}
    run_colors = {}
    amplicon_colors = {}

    au_styles = {}
    library_styles = {}

    query = """
    SELECT
        s.sample_id,
        s.label,

        l.library_id,

        au.analysis_unit_id,
        au.analysis_dataset_id,

        auf.sequencing_output_id,

        so.sequencing_run_id,
        so.amplicon_type_id

    FROM samples s

    LEFT JOIN libraries l
        ON l.sample_id = s.sample_id

    LEFT JOIN analysis_units au
        ON au.library_id = l.library_id

    LEFT JOIN analysis_unit_files auf
        ON auf.analysis_unit_id = au.analysis_unit_id

    LEFT JOIN sequencing_outputs so
        ON so.sequencing_output_id = auf.sequencing_output_id

    WHERE s.project_id = ?
    
    
    ORDER BY
        s.sample_id,
        l.library_id,
        au.analysis_unit_id,
        auf.sequencing_output_id

    """

    cur.execute(query, (project_id,))

    for row in cur.fetchall():

        (
            sample_id,
            sample_label,
            library_id,
            au_id,
            dataset_id,
            sequencing_output_id,
            sequencing_run_id,
            amplicon_type_id,
        ) = row

        sample_node = f"S{sample_id}"
        add_node(
            nodes,
            sample_node,
            sample_label or f"Sample {sample_id}"
        )

        #
        # LIBRARY
        #

        if not library_id:
            missing = f"ML{sample_id}"

            add_missing_node(
                nodes,
                classes,
                missing,
                "Missing Library",
            )

            add_edge(
                edges,
                sample_node,
                missing,
            )

            continue

        library_node = f"L{library_id}"

        add_node(
            nodes,
            library_node,
            f"Library {library_id}",
        )

        add_edge(
            edges,
            sample_node,
            library_node,
        )

        #
        # AMPLICON -> LIBRARY BORDER
        #

        library_styles.setdefault(
            library_node,
            {}
        )

        if amplicon_type_id:

            get_color(
                amplicon_type_id,
                amplicon_colors,
            )

            library_styles[
                library_node
            ]["amplicon"] = amplicon_type_id

        #
        # AU
        #

        if not au_id:

            missing = f"MAU{library_id}"

            add_missing_node(
                nodes,
                classes,
                missing,
                "Missing AU",
            )

            add_edge(
                edges,
                library_node,
                missing,
            )

            continue

        au_node = f"AU{au_id}"

        add_node(
            nodes,
            au_node,
            f"AU {au_id}",
        )

        add_edge(
            edges,
            library_node,
            au_node,
        )

        au_styles.setdefault(
            au_node,
            {}
        )

        #
        # DATASET -> AU FILL
        #

        if dataset_id:

            get_color(
                dataset_id,
                dataset_colors,
            )

            au_styles[
                au_node
            ]["dataset"] = dataset_id

        #
        # RUN -> AU BORDER
        #

        if sequencing_run_id:

            get_color(
                sequencing_run_id,
                run_colors,
            )

            au_styles[
                au_node
            ]["run"] = sequencing_run_id

        #
        # SO
        #

        if sequencing_output_id:

            so_node = (
                f"SO{sequencing_output_id}"
            )

            add_node(
                nodes,
                so_node,
                f"SO {sequencing_output_id}",
            )

            add_edge(
                edges,
                au_node,
                so_node,
            )
    conn.close()

    output = []

    output.append("graph LR")
    output.append("")

    output.extend(sorted(nodes, key=str))
    output.append("")

    output.extend(sorted(edges, key=str))
    output.append("")

    #
    # LEGENDS
    #

    output.append("subgraph Dataset_Legend")

    for dataset_id in sorted(dataset_colors):
        output.append(
            f'LEG_DS_{dataset_id}["Dataset {dataset_id}"]'
        )

    output.append("end")
    output.append("")

    output.append("subgraph Run_Legend")

    for run_id in sorted(run_colors):
        output.append(
            f'LEG_RUN_{run_id}["Run {run_id}"]'
        )

    output.append("end")
    output.append("")

    output.append("subgraph Amplicon_Legend")

    for amp_id in sorted(amplicon_colors):
        output.append(
            f'LEG_AMP_{amp_id}["Amplicon {amp_id}"]'
        )

    output.append("end")
    output.append("")

    #
    # DATASET CLASSES
    #

    for dataset_id, color in dataset_colors.items():

        output.append(
            f"classDef ds_{dataset_id} "
            f"fill:{color},"
            f"stroke:#444,"
            f"stroke-width:2px"
        )

        output.append(
            f"class LEG_DS_{dataset_id} "
            f"ds_{dataset_id}"
        )

    #
    # RUN CLASSES
    #

    for run_id, color in run_colors.items():

        output.append(
            f"classDef run_{run_id} "
            f"fill:#ffffff,"
            f"stroke:{color},"
            f"stroke-width:5px"
        )

        output.append(
            f"class LEG_RUN_{run_id} "
            f"run_{run_id}"
        )

    #
    # AMPLICON CLASSES
    #

    for amp_id, color in amplicon_colors.items():

        output.append(
            f"classDef amp_{amp_id} "
            f"fill:#ffffff,"
            f"stroke:{color},"
            f"stroke-width:5px"
        )

        output.append(
            f"class LEG_AMP_{amp_id} "
            f"amp_{amp_id}"
        )

    #
    # AU CLASSES
    #

    for au_node, style in au_styles.items():

        dataset_id = style.get(
            "dataset"
        )

        run_id = style.get(
            "run"
        )

        fill_color = (
            dataset_colors.get(
                dataset_id,
                "#ffffff"
            )
        )

        border_color = (
            run_colors.get(
                run_id,
                "#444444"
            )
        )

        class_name = (
            f"au_d{dataset_id}_r{run_id}"
        )

        output.append(
            f"classDef {class_name} "
            f"fill:{fill_color},"
            f"stroke:{border_color},"
            f"stroke-width:5px"
        )

        output.append(
            f"class {au_node} {class_name}"
        )

    #
    # LIBRARY CLASSES
    #

    for library_node, style in library_styles.items():

        amplicon_id = style.get(
            "amplicon"
        )

        if not amplicon_id:
            continue

        border_color = (
            amplicon_colors[
                amplicon_id
            ]
        )

        class_name = (
            f"lib_amp_{amplicon_id}"
        )

        output.append(
            f"classDef {class_name} "
            f"fill:#ffffff,"
            f"stroke:{border_color},"
            f"stroke-width:5px"
        )

        output.append(
            f"class {library_node} "
            f"{class_name}"
        )

    #
    # Missing
    #

    output.append(
        "classDef missing "
        "fill:#ff9999,"
        "stroke:#cc0000,"
        "stroke-width:3px"
    )

    output.extend(classes)

    output_file = (
        Path(__file__).resolve().parent.parent.parent
        / f"project_{project_id}.mmd"
    )

    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"Created {output_file}")


if __name__ == "__main__":
    main()