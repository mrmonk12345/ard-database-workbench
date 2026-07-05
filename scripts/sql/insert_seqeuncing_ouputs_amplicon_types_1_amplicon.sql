INSERT INTO sequencing_outputs_amplicon_types (
    sequencing_output_id,
    amplicon_type_id
)
SELECT
    so.sequencing_output_id,
    so.amplicon_type_id
FROM sequencing_outputs so
WHERE so.project_id = ?;