from PIL import Image
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from app.decorators import autosave
from app.models import TimestampedModel, DefaultQuerySet
from messaging.owl import Owl
from works.signals import signals

ON_MODERATION = 'on-moderation'
REVIEWED = 'reviewed'


class WorkQuerySet(DefaultQuerySet):
    def for_viewset(self) -> 'WorkQuerySet':
        return self.select_related(
            'reviews',
        )

    def on_moderation(self, *args, **kwargs) -> 'WorkQuerySet':
        return self.filter(status=ON_MODERATION)

    def reviewed(self, *args, **kwargs) -> 'WorkQuerySet':
        return self.filter(status=REVIEWED)


class Work(TimestampedModel):
    STATUSES = [
        (ON_MODERATION, _('On moderation')),
        (REVIEWED, _('Reviewed')),
    ]

    objects: 'WorkQuerySet' = WorkQuerySet.as_manager()

    status = models.CharField(choices=STATUSES, default=ON_MODERATION, max_length=100)
    username = models.CharField(_('username'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False)

    @autosave
    def to_moderation(self) -> None:
        self.status = ON_MODERATION

    @autosave
    def to_reviewed(self) -> None:
        if self.status == ON_MODERATION:
            self.status = REVIEWED

    def notify_user_by_email(self, template: str = 'user_notification.txt') -> None:
        owl = Owl(
            template=template,
            ctx={
                'work_id': self.pk,
            },
            from_email=settings.OUR_EMAIL,
            reply_to=settings.OUR_EMAIL,
            to=[self.email],
        )
        owl.send()


class WorkImage(TimestampedModel):
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
    thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFill(200, 200)], format='PNG',
    )

    def save(self, *args, **kwargs):
        super().save()
        signals.image_added.send(sender=self.__class__, work=self.work)


class Review(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    work = models.OneToOneField('Work', on_delete=models.CASCADE, related_name='reviews')
    first_score = models.IntegerField(_('First Score'), null=False, default=0)
    second_score = models.IntegerField(_('Second Score'), null=False, default=0)
    third_score = models.IntegerField(_('Third Score'), null=False, default=0)

    def save(self, *args, **kwargs):
        if self.work:
            self.work.to_reviewed()
            super().save()
            signals.review_added.send(sender=self.__class__, work=self.work)

    def get_absolute_url(self) -> str:
        return f'/admin/review/{self.pk}/'
