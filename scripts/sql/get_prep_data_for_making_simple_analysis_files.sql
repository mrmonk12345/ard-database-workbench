SELECT
    au.analysis_unit_id,
    au.analysis_unit_name,
    so.sequencing_output_id,
    so.fastq1,
    so.fastq2
FROM analysis_dataset_inputs adi
JOIN analysis_units au
    ON adi.analysis_unit_id = au.analysis_unit_id
JOIN libraries l
    ON l.library_id = au.library_id
JOIN sequencing_outputs so
    ON au.sequencing_run_id = so.sequencing_run_id
    AND l.sample_id = so.sample_id
JOIN sequencing_outputs_amplicon_types soat
   ON so.sequencing_output_id = soat.sequencing_output_id
   AND soat.amplicon_type_id = l.amplicon_type_id
WHERE adi.analysis_dataset_id = ?
  AND so.fastq1 IS NOT NULL
  AND so.fastq2 IS NOT NULL
  AND so.sequencing_output_id IN (
      SELECT sequencing_output_id
      FROM sequencing_outputs_amplicon_types
      GROUP BY sequencing_output_id
      HAVING COUNT(*) = 1
);
