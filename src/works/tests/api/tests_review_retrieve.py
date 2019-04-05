import pytest

from app.test.api_client import DRFClient

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def anon_api():
    return DRFClient(anon=True)


@pytest.fixture
def review(mixer, work):
    return mixer.blend('works.Review', work=work)


@pytest.mark.parametrize('fields', [[
    'id',
    'created',
    'modified',
    'username',
    'email',
    'status',
    'reviews',
]])
@pytest.mark.usefixtures('review')
def test_works_in_listing_has_required_fields(api, fields):
    got = api.get('/api/v1/reviews/')

    for field in fields:
        assert field in got[0]


@pytest.mark.parametrize('fields', [[
    'id',
    'created',
    'modified',
    'username',
    'email',
    'images',
    'status',
    'reviews',
]])
@pytest.mark.usefixtures('review')
def test_work_has_required_fields(api, fields, work):
    got = api.get(f'/api/v1/reviews/{work.pk}/')

    for field in fields:
        assert field in got


@pytest.mark.usefixtures('review')
def test_works_in_listing_access_from_anon_user(anon_api):
    anon_api.get('/api/v1/reviews/', expected_status_code=401)


@pytest.mark.usefixtures('review')
def test_work_access_from_anon_user(anon_api, work):
    anon_api.get(f'/api/v1/reviews/{work.pk}/', expected_status_code=401)

