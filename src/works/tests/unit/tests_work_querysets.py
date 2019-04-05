import pytest

from works.models import Work

pytestmark = [
    pytest.mark.django_db,
]


def test_included_work_in_on_moderation_queryset_by_default(work):
    assert work in Work.objects.on_moderation()


def test_excluded_work_in_reviewed_queryset_by_default(work):
    assert work not in Work.objects.reviewed()


def test_included_work_in_reviewed_queryset_after_got_review(work):
    work.to_reviewed()
    assert work in Work.objects.reviewed()


def test_excluded_work_in_on_moderation_queryset_after_got_review(work):
    work.to_reviewed()
    assert work not in Work.objects.on_moderation()


def test_included_work_in_for_viewset_queryset_by_default(work):
    assert work in Work.objects.for_viewset()


def test_included_work_in_for_viewset_queryset_after_got_review(work):
    work.to_reviewed()
    assert work in Work.objects.for_viewset()
