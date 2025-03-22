import pytest
import sqlite3
import polars as pl
import os
from src.db_loader import load_data


@pytest.fixture
def sample_parquet_file():
    parquet_path = os.path.join("data", "processed_data.parquet")
    # Read the full Parquet file and take 5 rows
    df = pl.read_parquet(parquet_path)
    sample_df = df.head(5)
    # Save the sample Parquet file
    sample_parquet_path = os.path.join("data", "sample_processed_data.parquet")
    sample_df.write_parquet(sample_parquet_path)
    return sample_parquet_path

@pytest.fixture
def sample_db_file(tmpdir):
    return str(tmpdir.join("test.db"))

def test_load_data_creates_table(sample_parquet_file, sample_db_file):
    load_data(sample_parquet_file, sample_db_file)
    conn = sqlite3.connect(sample_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
    assert cursor.fetchone() is not None
    conn.close()

def test_load_data_indexes_created(sample_parquet_file, sample_db_file):
    load_data(sample_parquet_file, sample_db_file)
    conn = sqlite3.connect(sample_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_year'")
    assert cursor.fetchone() is not None
    conn.close()

def test_load_data_indexes_created(sample_parquet_file, sample_db_file):
    load_data(sample_parquet_file, sample_db_file)
    conn = sqlite3.connect(sample_db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_title'")
    assert cursor.fetchone() is not None
    conn.close()