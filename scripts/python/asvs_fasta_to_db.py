import sqlite3
from pathlib import Path

from config import DATABASE_PATH

FASTA_FILE = "dna_sequences.fasta"
PIPELINE_RUN_ID = 6

fasta_path = Path("pipeline_runs") / str(PIPELINE_RUN_ID) / FASTA_FILE

conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()

records = []

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

            sequence_hash = line[1:]
            sequence_parts = []

        else:
            sequence_parts.append(line)

    if sequence_hash is not None:
        records.append((
            PIPELINE_RUN_ID,
            "".join(sequence_parts),
            sequence_hash
        ))

cur.executemany("""
    INSERT INTO asvs (
        pipeline_run_id,
        sequence,
        sequence_hash
    )
    VALUES (?, ?, ?)
""", records)

conn.commit()
conn.close()

print(f"Imported {len(records)} ASVs successfully.")