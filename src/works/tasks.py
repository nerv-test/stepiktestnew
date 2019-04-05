from django.apps import apps
from django.conf import settings

from app.celery import celery
from messaging.owl import Owl


@celery.task
def notify_user_by_email(work_id, template: str):
    if settings.DISABLE_NOTIFICATIONS:
        return

    work = apps.get_model('works.Work').objects.get(pk=work_id)
    work.notify_user_by_email(template=template)


@celery.task
def notify_moderator_by_email():
    if settings.DISABLE_NOTIFICATIONS:
        return

    work_on_moderation_count = apps.get_model('works.Work').objects.on_moderation().count()

    if work_on_moderation_count == 0:
        return

    owl = Owl(
        template='moderator_notification.txt',
        ctx={
            'work_on_moderation_count': work_on_moderation_count,
        },
        from_email=settings.OUR_EMAIL,
        reply_to=settings.OUR_EMAIL,
        to=[settings.OUR_EMAIL],  # any moderator's email
    )
    owl.send()
