"""Pytest configuration for the rag_clean workspace."""

pytest_plugins = ["tests.regression.conftest"]

# Exclude the manual runner script that shares a module name with the CLI variant.
collect_ignore = [
	"test_single_collection.py",
	"test_progress_output.py",
]


def pytest_configure(config):
	config.addinivalue_line(
		"markers",
		"regression_harness: Regression harness scenarios for Story 4.3.",
	)
