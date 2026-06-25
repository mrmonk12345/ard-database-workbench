SELECT DISTINCT
    at.*
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN libraries l
  ON au.library_id = l.library_id
JOIN amplicon_type at
    ON l.amplicon_type_id = at.amplicon_type_id
WHERE adi.analysis_dataset_id = ? ;
