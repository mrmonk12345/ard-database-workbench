#!/usr/bin/env python3

import sqlite3
import sys
from pathlib import Path

from config import DATABASE_PATH


def add_node(nodes, node_id, label):
    nodes.add(f'{node_id}["{label}"]')


def add_edge(edges, source, target):
    edges.add(f"{source} --> {target}")


def add_missing_node(nodes, classes, node_id, label):
    nodes.add(f'{node_id}["{label}"]')
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

    query = """
    SELECT

        s.sample_id,
        s.label,

        l.library_id,
        l.amplicon_type_id,

        au.analysis_unit_id,
        au.sequencing_run_id,
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
    """

    cur.execute(query, (project_id,))

    for row in cur.fetchall():

        (
            sample_id,
            sample_label,

            library_id,
            library_amplicon_id,

            au_id,
            au_run_id,
            dataset_id,

            sequencing_output_id,

            so_run_id,
            so_amplicon_id

        ) = row

        # SAMPLE

        sample_node = f"S{sample_id}"
        add_node(nodes, sample_node, sample_label)

        # LIBRARY

        if library_id:
            library_node = f"L{library_id}"
            add_node(nodes, library_node, f"Library {library_id}")
            add_edge(edges, sample_node, library_node)
        else:
            missing = f"ML{sample_id}"
            add_missing_node(nodes, classes, missing, "Missing Library")
            add_edge(edges, sample_node, missing)
            continue

        # LIBRARY -> AMPLICON

        if library_amplicon_id:
            amp_node = f"AT{library_amplicon_id}"
            add_node(nodes, amp_node, f"Amplicon {library_amplicon_id}")
            add_edge(edges, library_node, amp_node)

        # ANALYSIS UNIT

        if au_id:
            au_node = f"AU{au_id}"
            add_node(nodes, au_node, f"AU {au_id}")
            add_edge(edges, library_node, au_node)
        else:
            missing = f"MAU{library_id}"
            add_missing_node(nodes, classes, missing, "Missing AU")
            add_edge(edges, library_node, missing)
            continue

        # AU -> DATASET

        if dataset_id:
            dataset_node = f"DS{dataset_id}"
            add_node(nodes, dataset_node, f"Dataset {dataset_id}")
            add_edge(edges, au_node, dataset_node)
        else:
            missing = f"MDS{au_id}"
            add_missing_node(nodes, classes, missing, "Missing Dataset")
            add_edge(edges, au_node, missing)

        # AU -> RUN

        if au_run_id:
            run_node = f"SR{au_run_id}"
            add_node(nodes, run_node, f"Run {au_run_id}")
            add_edge(edges, au_node, run_node)

        # AU -> SEQUENCING OUTPUT

        print(
                  f"AU={au_id} "
                  f"SO={sequencing_output_id} "
                  f"type={type(sequencing_output_id)}"
              )
        if sequencing_output_id:
            so_node = f"SO{sequencing_output_id}"
            add_node(nodes, so_node, f"SO {sequencing_output_id}")
            add_edge(edges, au_node, so_node)
        else:
            missing = f"MSO{au_id}"
            add_missing_node(nodes, classes, missing, "Missing Output")
            add_edge(edges, au_node, missing)
            continue

        # SO -> RUN

        if so_run_id:
            run_node = f"SR{so_run_id}"
            add_node(nodes, run_node, f"Run {so_run_id}")
            add_edge(edges, so_node, run_node)

        # SO -> AMPLICON

        if so_amplicon_id:
            amp_node = f"AT{so_amplicon_id}"
            add_node(nodes, amp_node, f"Amplicon {so_amplicon_id}")
            add_edge(edges, so_node, amp_node)

    conn.close()

    output = []

    output.append("graph LR")
    output.append("")

    output.extend(sorted(nodes))
    output.append("")

    output.extend(sorted(edges))
    output.append("")

    output.append("classDef missing fill:#ff9999,stroke:#cc0000")
    output.extend(classes)

    output_file = (
        Path(__file__).resolve()
        .parent
        .parent
        .parent
        / f"project_{project_id}.mmd"
    )

    with open(output_file, "w") as f:
        f.write("\n".join(output))

    print(f"Created {output_file}")


if __name__ == "__main__":
    main()