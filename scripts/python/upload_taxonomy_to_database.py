
"""Load feature taxonomy assignments from a TSV file into the database."""

import argparse
import sqlite3
from datetime import date

import pandas as pd


def parse_taxonomy(taxon_string):
    """
    Convert a semicolon-separated taxonomy string into ranked values.

    Args:
        taxon_string: Taxonomy string using prefixes such as ``d__`` and
            ``p__``.

    Returns:
        A dictionary containing the standard taxonomic ranks.
    """

    ranks = {
        "kingdom": None,
        "phylum": None,
        "class": None,
        "order": None,
        "family": None,
        "genus": None,
        "species": None,
    }

    # Map taxonomy prefixes to database column names.
    rank_map = {
        "d": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
    }

    # Extract each rank from the taxonomy string.
    for item in str(taxon_string).split(";"):

        item = item.strip()

        if "__" not in item:
            continue

        prefix, value = item.split("__", 1)

        if prefix in rank_map and value:
            ranks[rank_map[prefix]] = value

    return ranks


def load_taxonomy(
    taxonomy_file,
    db_path,
    pipeline_run_id,
    reference,
):
    """
    Insert taxonomy assignments for features in a pipeline run.

    The TSV file must contain ``Feature ID``, ``Taxon``, and ``Confidence``
    columns. Features that are not present in the selected pipeline run are
    skipped.

    Args:
        taxonomy_file: Path to the taxonomy TSV file.
        db_path: Path to the SQLite database.
        pipeline_run_id: ID of the associated pipeline run.
        reference: the reference db used.
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Read the taxonomy assignments from the TSV file.
    df = pd.read_csv(
        taxonomy_file,
        sep="\t",
    )

    # Map sequence hashes to feature IDs for the selected pipeline run.
    feature_lookup = dict(
        cur.execute(
            """
            SELECT sequence_hash, feature_id
            FROM features
            WHERE pipeline_run_id = ?
            """,
            (pipeline_run_id,),
        )
    )

    rows = []

    # Convert each taxonomy assignment into database values.
    for _, row in df.iterrows():

        sequence_hash = row["Feature ID"]

        feature_id = feature_lookup.get(sequence_hash)

        if feature_id is None:
            continue

        taxonomy = parse_taxonomy(row["Taxon"])

        rows.append(
            (
                feature_id,
                taxonomy["kingdom"],
                taxonomy["phylum"],
                taxonomy["class"],
                taxonomy["order"],
                taxonomy["family"],
                taxonomy["genus"],
                taxonomy["species"],
                float(row["Confidence"]),
                reference,
                None,
            )
        )

    # Insert all taxonomy assignments in a single batch.
    cur.executemany(
        """
        INSERT INTO taxonomy (
            feature_id,
            kingdom,
            phylum,
            class,
            "order",
            family,
            genus,
            species,
            confidence,
            reference_db,
            date_classified
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(rows):,} taxonomy assignments")


if __name__ == "__main__":
    # Parse command-line arguments when the script is run directly.
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-run-id",
        required=True,
        type=int,
    )
    
    parser.add_argument(
        "--reference",
        required=True,
        type=str,
    )

    parser.add_argument(
        "--taxonomy",
        required=True,
    )

    parser.add_argument(
        "--db-path",
        required=True,
    )

    args = parser.parse_args()

    # Load the taxonomy assignments into the database.
    load_taxonomy(
        taxonomy_file=args.taxonomy,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
        reference = args.reference,
    )