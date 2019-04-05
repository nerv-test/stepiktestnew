import pytest

from works import signals

pytestmark = pytest.mark.django_db


def test_works_review_added_signal_send(work, mixer, connect_mock_handler):
    handler = connect_mock_handler(signals.review_added)

    mixer.blend('works.Review', work=work)

    assert handler.call_count == 1


def test_works_image_added_signal_send(work, mixer, connect_mock_handler):
    handler = connect_mock_handler(signals.image_added)

    mixer.blend('works.WorkImage', work=work)

    assert handler.call_count == 1
