
import sqlite3

DB_PATH = "project.db"


def load_samples(samples):
    conn =  sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for s in samples:

        cur.execute("""
            INSERT INTO samples (
                sample_name,
                original_sample_label,
                sample_label,
                project_id,
                initial_health_status,
                final_health_status,
                location_id,
                rootstock_id,
                sampling_compartment_id,
                treatment_id,
                time_since_planting,
                host_species,
                scion_cultivar,
                soil_texture,
                soil_type,
                sampling_depth,
                experimental_setting
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s.get("sample_name"),
            s.get("original_sample_label"),
            s.get("sample_label"),
            s.get("project_id"),
            s.get("initial_health_status"),
            s.get("final_health_status"),
            s.get("location_id"),
            s.get("rootstock_id"),
            s.get("sampling_compartment_id"),
            s.get("treatment_id"),
            s.get("time_since_planting"),
            s.get("host_species"),
            s.get("scion_cultivar"),
            s.get("soil_texture"),
            s.get("soil_type"),
            s.get("sampling_depth"),
            s.get("experimental_setting")
        ))


        print(f"[ADD] {s['sample_label']}")

    conn.commit()
    conn.close()