UPDATE sampling_compartments
SET project_id = (
    SELECT CASE
        WHEN COUNT(DISTINCT s.project_id) = 1
        THEN MIN(s.project_id)
        ELSE NULL
    END
    FROM samples s
    WHERE s.sampling_compartment_id = sampling_compartments.sampling_compartment_id
);