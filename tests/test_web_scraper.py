import pytest
import os
import csv
import requests
from src.web_scraper import fetch_data
from unittest.mock import patch, Mock

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("MY_KEY", "test_key")
    monkeypatch.setenv("MY_HOST", "test_host")


@patch('requests.get')
def test_fetch_data_failure(mock_get, mock_env):
    mock_get.side_effect = requests.exceptions.RequestException("Failed to fetch data")
    file_path = fetch_data()
    assert file_path is None