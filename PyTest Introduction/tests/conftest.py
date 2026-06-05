import pytest
import pandas as pd
import re

# Fixture to read the CSV file
@pytest.fixture(scope="session")
def read_csv_file():
    def _read_csv_file(path_to_file):
        df = pd.read_csv(path_to_file)
        assert not df.empty, (f"CSV file '{path_to_file}' is empty")
        return df
    return _read_csv_file

# Fixture to validate the schema of the file
@pytest.fixture(scope="session")
def validate_schema():
    def _validate_schema(actual_schema, expected_schema):
        return list(actual_schema) == list(expected_schema)
    return _validate_schema

# Fixture to validate the email format
@pytest.fixture(scope="session")
def validate_email_format():
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    def _validate_email_format(email):
        return bool(re.match(email_pattern, str(email)))
    return _validate_email_format

# Fixture to validate the duplicate rows
@pytest.fixture(scope="session")
def get_duplicate_rows():
    def _get_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
        return df[df.duplicated(keep=False)]
    return _get_duplicate_rows


# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(items):
    for item in items:
        existing_markers = [mark.name for mark in item.iter_markers()]
        print(f"{item.name}: {existing_markers}")
        
        if not existing_markers:
            item.add_marker(pytest.mark.unmarked)