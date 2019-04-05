from django.conf import settings
from django.dispatch import receiver

from app.pdf import PDFDocument
from works import signals, tasks


@receiver(signals.review_added)
def notify_user_about_new_review(sender, **kwargs):
    tasks.notify_user_by_email.delay(kwargs['work'].pk, template='user_notification.txt')


@receiver(signals.image_added, dispatch_uid='image_added')
def create_pdf(sender, **kwargs):
    """
    Create a thumbnail of image
    """
    work = kwargs['work']
    document = PDFDocument(template_name='pdf/work.html', work=work)
    with open(f'{settings.MEDIA_ROOT}test.pdf', 'wb') as f:
        f.write(document.render_pdf())
