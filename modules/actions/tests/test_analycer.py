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


def test_get_latest_files_returns_most_recent(dummy_analyser, tmp_path):
    importer_name = "dummy"
    items = [
        {"account_id": "123", "account_name": "dev"},
        {"account_id": "456", "account_name": "prod"},
    ]
    paths = []
    for item in items:
        base = tmp_path / f"{item['account_name']}_{item['account_id']}/json/{importer_name}/"
        dates = ["2025-10-01", "2025-10-09", "2025-09-30"]
        for d in dates:
            path = base / d
            path.mkdir(parents=True, exist_ok=True)
            if d == "2025-10-09":
                file = path / f"{importer_name}.json"
                file.write_text('{"ok": true}')
                paths.append(str(file))

    result = dummy_analyser.get_latest_files(items, importer_name)
    assert set(result) == set(paths)


def test_get_latest_files_ignores_invalid_dirs(dummy_analyser, tmp_path):
    importer_name = "dummy"
    items = [{"account_id": "999", "account_name": "test"}]

    
    base = tmp_path / "test_999/json/dummy/"
    (base / "not-a-date").mkdir(parents=True, exist_ok=True)
    (base / "2025-10-09").mkdir(parents=True, exist_ok=True)
    file = base / "2025-10-09/dummy.json"
    file.write_text('{"ok": true}')

    result = dummy_analyser.get_latest_files(items, importer_name)

  
    assert result == [str(file)]


def test_get_latest_files_empty_if_no_dir(dummy_analyser):
    importer_name = "dummy"
    items = [{"account_id": "123", "account_name": "missing"}]

    result = dummy_analyser.get_latest_files(items, importer_name)

    assert result == []