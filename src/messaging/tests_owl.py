from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core import mail
from django.test import override_settings
from django.utils import timezone

from messaging.owl import Owl


@pytest.fixture
def owl():
    def owl(to=None, **kwargs):
        if to is None:
            to = ['voldemar.krs@gmail.com']
        return Owl(
            template='mail/test.html',
            ctx={
                'username': 'abraham.lincoln',
                'full_name': 'Abraham Lincoln',
                'register_date': '12.09.1809',
                'time': timezone.now() - timedelta(days=1),
            },
            to=to,
            **kwargs,
        )
    return owl


@override_settings(DISABLE_NOTIFICATIONS=False, EMAIL_ENABLED=True)
def test_send(owl):
    owl = owl()
    owl.send()
    assert len(mail.outbox) == 1


@override_settings(DISABLE_NOTIFICATIONS=True)
def test_global_kill_switch(owl):
    owl = owl()
    owl.send()
    assert len(mail.outbox) == 0


@override_settings(DISABLE_NOTIFICATIONS=False, EMAIL_ENABLED=False)
def test_email_kill_switch(owl):
    owl = owl()
    owl.send()
    assert len(mail.outbox) == 0


def test_subject(owl):
    owl = owl()
    assert 'сабжекта для abraham.lincoln' in owl.msg.subject


def test_body(owl):
    owl = owl()
    assert 'Abraham Lincoln' in owl.msg.body
    assert '12.09.1809' in owl.msg.body
    assert 'abraham.lincoln' in owl.msg.body


def test_email_from(owl):
    owl = owl(from_email='ttt@test.org')
    m = owl.msg
    assert m.from_email == 'ttt@test.org'


def test_add_cc(owl):
    owl = owl()
    owl.add_cc('support@microsoft.com', 'legal@centrobank.ru')
    assert owl.msg.cc == ['support@microsoft.com', 'legal@centrobank.ru']


@override_settings(EMAIL_NOTIFICATIONS_FROM='ttt@test.org')
def test_email_from_default(owl):
    owl = owl()
    assert owl.msg.from_email == 'ttt@test.org'


@override_settings(REPLY_TO='reply@to.to')
def test_default_reply_to(owl):
    owl = owl()
    assert 'reply@to.to' in owl.msg.reply_to


def test_configurable_reply_to(owl):
    owl = owl(reply_to='Test reply to <test@reply.to>')
    assert 'Test reply to <test@reply.to>' in owl.msg.reply_to


def test_attaching(owl):
    owl = owl()
    owl.attach(filename='testing_file_name_100500.txt', content=b'just testing')

    assert len(owl.msg.attachments) == 1
    assert 'testing_file_name_100500.txt' in owl.msg.attachments[0]


def test_bad_to_address_does_not_send_message(owl):
    owl = owl(to=[])
    with patch.object(owl.msg, 'send') as send:
        owl.send()
        assert send.call_count == 0
