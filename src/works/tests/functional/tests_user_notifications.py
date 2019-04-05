import pytest

from works import tasks

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def change_settings(settings):
    settings.DISABLE_NOTIFICATIONS = False
    settings.EMAIL_ENABLED = True
    settings.OUR_EMAIL = 'stepik@stepik.stepik'


@pytest.fixture
def email(mailoutbox):
    return lambda: mailoutbox[0]


def test_should_send_one_email(work, mailoutbox):
    work.notify_user_by_email()

    assert len(mailoutbox) == 1


def test_should_send_email_with_correct_data(work, email):
    work.notify_user_by_email()

    assert email().to == ['i@will.worry']
    assert email().from_email == 'stepik@stepik.stepik'
    assert 'stepik@stepik.stepik' in email().reply_to


def test_should_send_with_correct_content(work, email):
    work.notify_user_by_email()

    assert f'Ваша работа №{work.pk} была одобрена модератором.' in email().body


def test_should_send_using_task(work, mailoutbox):
    tasks.notify_user_by_email.delay(work.pk, template='user_notification.txt')

    assert len(mailoutbox) == 1


def test_should_not_send_when_notifications_disabled(work, settings, mailoutbox):
    settings.DISABLE_NOTIFICATIONS = True
    tasks.notify_user_by_email.delay(work.pk, template='user_notification.txt')

    assert len(mailoutbox) == 0
