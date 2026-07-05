UPDATE analysis_units
SET analysis_unit_name = (
    SELECT 'sample' || l.sample_id || '_AU' || analysis_units.analysis_unit_id
    FROM libraries l
    WHERE l.library_id = analysis_units.library_id
)
WHERE (analysis_unit_name IS NULL OR analysis_unit_name = '');
