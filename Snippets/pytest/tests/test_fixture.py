import pytest

@pytest.fixture
def sample_data():
    return {"name": "Radek", "role": "QA Engineer"}

def test_with_fixture(sample_data):
    assert sample_data["role"] == "QA Engineer"
