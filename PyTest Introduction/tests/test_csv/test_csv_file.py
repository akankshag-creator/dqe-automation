import pytest
import re


def test_file_not_empty(read_csv_file):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    assert len(df) > 0

@pytest.mark.validate_csv
@pytest.mark.xfail(reason="Known issue: source file may contain duplicate records")
def test_duplicates(read_csv_file, get_duplicate_rows):

    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    duplicate_rows = get_duplicate_rows(df)
    assert duplicate_rows.empty, (f"Found {len(duplicate_rows)} duplicate rows:\n" f"{duplicate_rows}")

@pytest.mark.validate_csv
def test_validate_schema(read_csv_file, validate_schema):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    expected_schema = ["id","name","age","email","is_active"]
    
    assert validate_schema(df.columns, expected_schema), (f"Schema mismatch. ")

@pytest.mark.validate_csv
def test_age_column_valid(read_csv_file):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    invalid_age = df[(df["age"] < 0) |(df["age"] > 100)]
    assert invalid_age.empty, (f"Invalid age values found:\n{invalid_rows}")

@pytest.mark.skip(reason="Age validation not required")
def test_age_column_valid(read_csv_file):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    invalid_age = df[(df["age"] < 0) |(df["age"] > 100)]
    assert invalid_age.empty


@pytest.mark.validate_csv
def test_email_column_valid(read_csv_file, validate_email_format):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    invalid_emails = [email for email in df["email"] if not validate_email_format(email)]
    assert not invalid_emails, f"Invalid emails found: \n{invalid_emails}"


@pytest.mark.validate_csv
@pytest.mark.parametrize("user_id, expected_is_active",[(1, False),(2, True)])
def test_active_players(read_csv_file, user_id, expected_is_active):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    matching_rows = df[df["id"] == user_id]
    assert not matching_rows.empty, f"id={user_id} not found in file"
    actual_value = matching_rows["is_active"].iloc[0]
    assert actual_value == expected_is_active

def test_active_player(read_csv_file, expected_is_active):
    df = read_csv_file("PyTest Introduction\src\data\data.csv")
    matching_rows = df[df["id"] == 2]
    assert not matching_rows.empty, f"id=2 not found in file"
    actual_value = matching_rows["is_active"].iloc[0]
    assert actual_value == expected_is_active