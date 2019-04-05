import pytest

from app.test.api_client import DRFClient
from works.models import Review, Work

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def anon_api():
    return DRFClient(anon=True)


def test_review_creation(api, work):
    api.post('/api/v1/reviews/', {
        'work': work.pk,
        'first_score': 5,
        'second_score': 5,
        'third_score': 2,
    })

    created = Review.objects.first()
    assert Review.objects.exists()
    assert Work.objects.all().count() == 1
    assert created.work.pk == work.pk
    assert created.work.status == 'reviewed'
    assert created.first_score == 5
    assert created.second_score == 5
    assert created.third_score == 2


def test_review_creation_from_anon_user(anon_api, work):
    anon_api.post('/api/v1/reviews/', {
        'work': work.pk,
        'first_score': 5,
        'second_score': 5,
        'third_score': 2,
    }, expected_status_code=401)

    assert not Review.objects.exists()
