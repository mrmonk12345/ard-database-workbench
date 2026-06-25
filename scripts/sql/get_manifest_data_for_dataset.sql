SELECT
    au.analysis_unit_name,
    auf.read1_path,
    auf.read2_path
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN analysis_unit_files auf
    ON au.analysis_unit_id = auf.analysis_unit_id
WHERE adi.analysis_dataset_id = ?
  AND auf.read1_path IS NOT NULL
  AND auf.read2_path IS NOT NULL;
