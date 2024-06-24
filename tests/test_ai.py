import os
import pytest
from unittest.mock import MagicMock
from src.ai import run_prompt, extract_imports, split_methods

@pytest.fixture
def mock_openai_client(mocker):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Mocked response"))]
    )
    return mock_client

@pytest.fixture
def set_env_vars(mocker):
    mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"})

@pytest.mark.usefixtures("set_env_vars")
def test_run_prompt(mock_openai_client, mocker):
    mocker.patch('src.ai.OpenAI', return_value=mock_openai_client)
    response = run_prompt("Test prompt", "Test content")
    assert response == "Mocked response"
    mock_openai_client.chat.completions.create.assert_called_with(
        model="gpt-4-turbo", max_tokens=750, messages=[{"role": "user", "content": "Test prompt Test content"}]
    )

def test_extract_imports(tmpdir):
    test_file = tmpdir.join("test_file.py")
    test_file.write("import os\nimport sys\nprint('Hello')")
    imports = extract_imports(str(test_file))
    assert imports == ["import os", "import sys"]

def test_split_methods(tmpdir):
    test_file = tmpdir.join("test_file.py")
    code_content = """
def foo():
    print("foo")

def bar():
    print("bar")
"""
    test_file.write(code_content)
    methods = split_methods(str(test_file))
    assert len(methods) == 2
