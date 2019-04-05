import pytest


@pytest.fixture
def work(mixer):
    return mixer.blend('works.Work', email='i@will.worry')
