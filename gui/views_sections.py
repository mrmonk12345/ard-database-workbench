"""Define SQL-view dashboard sections and their related actions."""

from scripts.python.db_get_data import (
	get_ncbi_view,
	get_pipeline_runs_view,
)


def ncbi_view_section(window):
	"""Return the NCBI sample-run view section configuration."""
	return {
		"title": "NCBI Sample Run Info",
		"count": len(get_ncbi_view()),
		"buttons": [
			(
				"View",
				lambda: window.open_table(
					"NCBI Sample Run Info",
					get_ncbi_view(),
					"ncbi_sample_run_info.tsv",
				),
			),
		],
	}


def pipeline_runs_view_section(window):
	"""Return the pipeline-run summary view section configuration."""
	return {
		"title": "Pipeline Run Summary",
		"count": len(get_pipeline_runs_view()),
		"buttons": [
			(
				"View",
				lambda: window.open_table(
					"Pipeline Run Summary",
					get_pipeline_runs_view(),
					"pipeline_run_summary.tsv",
				),
			),
		],
	}
