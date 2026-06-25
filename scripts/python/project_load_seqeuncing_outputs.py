import sqlite3

DB_PATH = "project.db"


def load_sequencing_outputs(sequencing_outputs):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for so in sequencing_outputs:
        cur.execute("""
            INSERT INTO sequencing_outputs (
                sequencing_output_label,
                project_id,
                sample_id,
                sequencing_run_id,
                amplicon_type_id,
                srr,
                fastq1,
                fastq2,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            so["sequencing_output_label"],
            so["project_id"],
            so["sample_id"],
            so["sequencing_run_id"],
            so["amplicon_type_id"],
            so.get("srr"),
            so.get("fastq1"),
            so.get("fastq2"),
            so.get("notes"),
        ))

        print(f"[ADD] {so['sequencing_output_label']}")

    conn.commit()
    conn.close()
