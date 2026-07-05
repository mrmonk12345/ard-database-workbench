SELECT
    au.analysis_unit_name,
    s.sample_id,
    s.project_id,
    s.treatment_id,
    t.name AS treatment_name
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN libraries l
    ON l.library_id = au.library_id
JOIN samples s
    ON s.sample_id = l.sample_id
JOIN treatments t
    ON t.treatment_id = s.treatment_id
WHERE adi.analysis_dataset_id = ? ;
