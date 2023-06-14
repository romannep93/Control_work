import os
import pytest


@pytest.fixture
def create_temp_file(tmpdir):
    file_path = str(tmpdir.join("temp_file.txt"))
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def test_links():
    return ["https://www.google.com", "invalid_link"]
