"""Import ASV sequences from a pipeline FASTA file into the database."""

import sqlite3
from pathlib import Path

from config import DATABASE_PATH

FASTA_FILE = "dna_sequences.fasta"
PIPELINE_RUN_ID = 6

# Build the path to the FASTA file for the selected pipeline run.
fasta_path = Path("pipeline_runs") / str(PIPELINE_RUN_ID) / FASTA_FILE

# Open the database and prepare a cursor for inserting ASV records.
conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()

records = []

# Read the FASTA file and group sequence lines by their header.
with open(fasta_path) as f:
    sequence_hash = None
    sequence_parts = []

    for line in f:
        line = line.strip()

        if line.startswith(">"):
            if sequence_hash is not None:
                records.append((
                    PIPELINE_RUN_ID,
                    "".join(sequence_parts),
                    sequence_hash
                ))

            # FASTA headers contain the sequence hash after ">".
            sequence_hash = line[1:]
            sequence_parts = []

        else:
            # FASTA sequences may span multiple lines.
            sequence_parts.append(line)

    # Save the final record in the file.
    if sequence_hash is not None:
        records.append((
            PIPELINE_RUN_ID,
            "".join(sequence_parts),
            sequence_hash
        ))

# Insert all parsed ASV records into the database.
cur.executemany("""
    INSERT INTO asvs (
        pipeline_run_id,
        sequence,
        sequence_hash
    )
    VALUES (?, ?, ?)
""", records)

# Save the changes and close the database connection.
conn.commit()
conn.close()

print(f"Imported {len(records)} ASVs successfully.")