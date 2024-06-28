import os
from unittest import mock
import pytest
from src.ai import describe_file_contents
from unittest.mock import patch, mock_open

from src.main import traverse_directory

IGNORED_FILES = {'ignore_me.txt', 'skip_this.py'}
code_file_extensions = {'.py', '.js', '.ts'}
existing_files = {'exists.py'}
non_existing_files = {'new_file.py'}
existing_test_files = {os.path.join("tests", "test_exists.py")}
non_existing_test_files = {os.path.join("tests", "test_new_file.py")}

def describe_file_contents(file_path):
    return f"Description for {file_path}"

@pytest.fixture
def mock_os_walk():
    return [
        ('/root', ('subdir',), ('valid.py', 'ignore_me.txt')),
        ('/root/subdir', (), ('test_something.py', 'new.py'))
    ]

@pytest.fixture
def setup_gitignore(mock):
    content = "ignore_me.txt\n.env\nconfig.yml"
    mock("/root/.gitignore", "r", mock_open(read_data=content))

@pytest.fixture
def mock_exists():
    return lambda path: path in existing_files

@pytest.fixture
def mock_not_exists():
    return lambda path: path not in existing_files and path not in existing_test_files

@pytest.fixture
def mock_describe_file(fun):
    return mock.patch('src.main.describe_file', side_effect=fun)

@pytest.fixture
def setup_directory_and_files():
    with patch('os.walk') as mock_walk, \
         patch('os.path.exists') as mock_exists, \
         patch('src.main.describe_file_contents') as mock_describe:
        mock_walk.return_value = mock_os_walk
        mock_exists.side_effect = mock_not_exists
        mock_describe.side_effect = describe_file_contents
        yield

def test_traverse_directory_with_existing_tests(setup_directory_and_files):
    with patch("builtins.print") as mock_print:
        traverse_directory("/root", language="python")
        mock_print.assert_any_call("Skipping /root/tests/test_valid.py as it already exists.")
