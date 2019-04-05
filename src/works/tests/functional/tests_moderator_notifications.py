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


@pytest.mark.usefixtures('work')
def test_should_send_one_email(mailoutbox):
    tasks.notify_moderator_by_email.delay()

    assert len(mailoutbox) == 1


@pytest.mark.usefixtures('work')
def test_should_send_email_with_correct_data(email):
    tasks.notify_moderator_by_email.delay()

    assert email().to == ['stepik@stepik.stepik']
    assert email().from_email == 'stepik@stepik.stepik'
    assert 'stepik@stepik.stepik' in email().reply_to


@pytest.mark.usefixtures('work')
def test_should_send_with_correct_content(email):
    tasks.notify_moderator_by_email.delay()

    assert f'У вас есть 1 работ для проверки.' in email().body


@pytest.mark.usefixtures('work')
def test_should_not_send_when_notifications_disabled(settings, mailoutbox):
    settings.DISABLE_NOTIFICATIONS = True
    tasks.notify_moderator_by_email.delay()

    assert len(mailoutbox) == 0


def test_should_not_send_when_count_of_work_is_zero(work, mailoutbox):
    work.to_reviewed()
    tasks.notify_moderator_by_email.delay()

    assert len(mailoutbox) == 0
