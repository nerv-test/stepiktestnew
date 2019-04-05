import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_default_status(work):
    assert work.status == 'on-moderation'


def test_change_status_to_reviewed(work):
    work.to_reviewed()
    assert work.status == 'reviewed'


def test_change_status_to_moderation(mixer):
    work = mixer.blend('works.Work', status='reviewed')

    assert work.status == 'reviewed'
    work.to_moderation()
    assert work.status == 'on-moderation'
