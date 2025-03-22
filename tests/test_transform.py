import pytest
import polars as pl
import os
import pytest
import polars as pl
from src.data_transform import clean_data

@pytest.fixture
def sample_csv_file():
    csv_path = os.path.join("data", "top250movies.csv")
    # Read the full CSV file and take the first 5 rows
    df = pl.read_csv(csv_path)
    sample_df = df.head(5)
    # Save the sample CSV file
    sample_csv_path = os.path.join("data", "sample_top250movies.csv")
    sample_df.write_csv(sample_csv_path)
    return sample_csv_path

def test_clean_data_missing_values(sample_csv_file):
    df = clean_data(sample_csv_file)
    # Check if missing values are handled correctly
    assert df["primaryTitle"].null_count() == 0, "Missing values found in primaryTitle column"
    assert df["startYear"].null_count() == 0, "Missing values found in startYear column"

def test_clean_data_duplicates(sample_csv_file):
    df = clean_data(sample_csv_file)
    # Check if duplicates are removed based on the 'id' column
    assert df["id"].is_unique().all(), "Duplicate IDs found in the cleaned DataFrame"

def test_clean_data_numeric_transformation(sample_csv_file):
    df = clean_data(sample_csv_file)
    # Check if numeric columns are correctly converted to Float64
    assert df["startYear"].dtype == pl.Float64
    assert df["runtimeMinutes"].dtype == pl.Float64

def test_clean_data_date_column(sample_csv_file):
    df = clean_data(sample_csv_file)
    # Validate date column parsing
    assert df["releaseDate"].dtype == pl.Date, "releaseDate column is not of type Date"
