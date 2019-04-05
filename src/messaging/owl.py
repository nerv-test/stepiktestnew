import pytz
from django.conf import settings
from mail_templated import EmailMessage


class Owl():
    """
    Owl is an email agent. It utilizes default send_mail() as a message-backend,
    hoping you have configured it properly. On the production host it tries to
    queue your message via the Celery daemon.

    For usage examples please see tests.
    """

    timezone = None

    def __init__(self, template, ctx, from_email=None, reply_to=None, timezone=None, to=None):
        if to is None:
            to = []
        if from_email is None:
            from_email = settings.EMAIL_NOTIFICATIONS_FROM
        if reply_to is None:
            reply_to = settings.REPLY_TO

        self.template = template
        self.ctx = ctx
        self.to = to
        self.reply_to = reply_to
        self.from_email = from_email

        if timezone is not None:
            if isinstance(timezone, str):
                self.timezone = pytz.timezone(timezone)
            else:
                self.timezone = timezone

        self.headers = {
            'X-GM-Timezone': str(self.timezone),
        }

        self.EmailMessage()

    def EmailMessage(self):
        """
        This method preventively renders a message to catch possible errors in the
        main flow.
        """
        self.msg = EmailMessage(
            self.template,
            self.ctx,
            self.from_email,
            self.to,
            headers=self.headers,
            reply_to=[self.reply_to],
        )
        self.msg.render()

    def send(self):
        """
        Send message

        """
        if not self.clean():
            return

        if not settings.DISABLE_NOTIFICATIONS and settings.EMAIL_ENABLED:
            self.msg.send()

    def add_cc(self, *args):
        """
        Add a list of recipients
        """
        self.msg.cc += args

    def attach(self, filename=None, content=None, mimetype=None):
        """
        Add an attachment to the message

        See http://django-mail-templated.readthedocs.io/en/master/api.html?highlight=attach#mail_templated.EmailMessage.attach
        """
        return self.msg.attach(filename, content, mimetype)

    def clean(self) -> bool:
        if not self.to or not self.to[0]:
            return False

        return True
