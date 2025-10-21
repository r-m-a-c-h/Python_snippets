import pytest

@pytest.mark.skip(reason="Not yet implemented")
def test_not_ready():
    pass

@pytest.mark.slow
def test_slow_process():
    import time
    time.sleep(2)
    assert True
