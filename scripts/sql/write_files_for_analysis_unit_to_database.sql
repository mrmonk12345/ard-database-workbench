INSERT INTO analysis_unit_files (
    analysis_unit_id,
    sequencing_output_id,
    read1_path,
    read2_path,
    gzip_done
) VALUES (?, ?, ?, ?, 1)
ON CONFLICT(analysis_unit_id) DO UPDATE SET
    sequencing_output_id = excluded.sequencing_output_id,
    read1_path = excluded.read1_path,
    read2_path = excluded.read2_path,
    gzip_done = 1;
