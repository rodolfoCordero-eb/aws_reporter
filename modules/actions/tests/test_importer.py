import pytest
import os
import json
from src.actions.importer import Importer 
from datetime import datetime


class DummyImporter(Importer):

    def __init__(self, path="/tmp/"):
        super().__init__(path)
    def name(self):
        return "testfile"

    def run(self, session, acc_id, acc_name, region):
        pass


@pytest.fixture
def dummy_importer(tmp_path):

    # tmp_path es un fixture de pytest que crea un directorio temporal seguro
    return DummyImporter(path=str(tmp_path))


def test_write_to_file_creates_json(dummy_importer):
    # Arrange
    content = {"key": "value"}
    full_path = f"{dummy_importer.path}/"
    os.makedirs(full_path, exist_ok=True)

    # Act
    dummy_importer.write_to_file(full_path, content)

    # Assert
    file_path = os.path.join(full_path, "testfile.json")
    assert os.path.exists(file_path)
    with open(file_path) as f:
        data = json.load(f)
    assert data == content


def test_save_creates_directory_and_writes_file(dummy_importer):
    content = {"test": 123}

    acc_id = "123456789012"
    acc_name = "dev"

    # Act
    dummy_importer.save(acc_id, acc_name, content)

    # Assert
    now = datetime.now()
    expected_dir = f"{dummy_importer.path}/{acc_name}_{acc_id}/json/testfile/{now.strftime("%Y-%m-%d")}/"
    expected_file = os.path.join(expected_dir, "testfile.json")
    assert os.path.exists(expected_dir)
    assert os.path.exists(expected_file)
    with open(expected_file) as f:
        data = json.load(f)
    assert data == content
