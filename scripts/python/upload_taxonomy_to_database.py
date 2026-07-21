import argparse
import sqlite3
from datetime import date

import pandas as pd


def parse_taxonomy(taxon_string):

    ranks = {
        "kingdom": None,
        "phylum": None,
        "class": None,
        "order": None,
        "family": None,
        "genus": None,
        "species": None,
    }

    rank_map = {
        "d": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
    }

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
):

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    df = pd.read_csv(
        taxonomy_file,
        sep="\t",
    )

    asv_lookup = dict(
        cur.execute(
            """
            SELECT sequence_hash, asv_id
            FROM asvs
            WHERE pipeline_run_id = ?
            """,
            (pipeline_run_id,),
        )
    )

    rows = []

    for _, row in df.iterrows():

        sequence_hash = row["Feature ID"]

        asv_id = asv_lookup.get(sequence_hash)

        if asv_id is None:
            continue

        taxonomy = parse_taxonomy(row["Taxon"])

        rows.append(
            (
                asv_id,
                taxonomy["kingdom"],
                taxonomy["phylum"],
                taxonomy["class"],
                taxonomy["order"],
                taxonomy["family"],
                taxonomy["genus"],
                taxonomy["species"],
                float(row["Confidence"]),
                "GTDB",
                date.today().isoformat(),
            )
        )

    cur.executemany(
        """
        INSERT INTO taxonomy (
            asv_id,
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

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline-run-id",
        required=True,
        type=int,
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

    load_taxonomy(
        taxonomy_file=args.taxonomy,
        db_path=args.db_path,
        pipeline_run_id=args.pipeline_run_id,
    )