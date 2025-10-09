import os
import pytest
from pathlib import Path
from src.actions.analycer import Analycer  


class DummyAnalycer(Analycer):
    def __init__(self, path="/tmp/"):
        super().__init__(path)

    def run(self, items: dict, importer_name: str, output_path: str):
        pass

    def name(self):
        return "dummy"


@pytest.fixture
def dummy_analyser(tmp_path):
    return DummyAnalycer(path=tmp_path)

def test_get_files_returns_existing_files(dummy_analyser, tmp_path):

    items = [
        {'account_id': '123', 'account_name': 'dev', 'date': '2025-10-09'},
        {'account_id': '456', 'account_name': 'prod', 'date': '2025-10-08'},
    ]
    importer_name = "dummy"

    file_path = tmp_path / "dev_123/json/dummy/2025-10-09/dummy.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text('{"key":"value"}')

    # Act
    result = dummy_analyser.get_files(items, importer_name)

    # Assert
    expected = [str(file_path)]
    assert result == expected

def test_get_files_returns_empty_if_no_files(dummy_analyser):
    items = [
        {'account_id': '000', 'account_name': 'missing', 'date': '2025-01-01'}
    ]
    importer_name = "dummy"

    result = dummy_analyser.get_files(items, importer_name)

    assert result == []

def test_get_files_multiple_files(dummy_analyser, tmp_path):
    items = [
        {'account_id': '123', 'account_name': 'dev', 'date': '2025-10-09'},
        {'account_id': '456', 'account_name': 'prod', 'date': '2025-10-08'},
        {'account_id': '4526', 'account_name': 'stg', 'date': '2025-11-08'},
    ]
    importer_name = "dummy"

    paths = []
    for item in items:
        path = tmp_path / f"{item['account_name']}_{item['account_id']}/json/{importer_name}/{item['date']}/{importer_name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"key":"value"}')
        paths.append(str(path))

    result = dummy_analyser.get_files(items, importer_name)
    assert set(result) == set(paths)
