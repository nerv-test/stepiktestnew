import os
import tempfile

import pytest
from PIL import Image

from app.test.api_client import DRFClient
from works.models import Work, WorkImage

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def api():
    return DRFClient(anon=True)


@pytest.fixture()
def image():
    def inner(suffix='.jpg'):
        image = Image.new('RGB', (300, 300))
        tmp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        image.save(tmp_file)
        return tmp_file
    return inner


@pytest.mark.parametrize('image_format', (
    '.jpg',
    '.png',
    '.gif',
))
def test_work_creation(api, image, image_format):
    file = image(image_format)
    with open(file.name, 'rb') as data:
        api.post('/api/v1/works/', {
            'username': 'testuser',
            'email': 'stepik@stepik.stepik',
            'image': data,
        }, format='multipart')

    created = Work.objects.first()
    assert WorkImage.objects.exists()
    assert created.username == 'testuser'
    assert created.email == 'stepik@stepik.stepik'
    assert os.path.basename(file.name) in created.images.first().image.url


@pytest.mark.parametrize('dict_key', (
    'username',
    'email',
))
def test_work_creation_without_any_required_field_must_fail(api, image, dict_key):
    file = image('.jpg')
    with open(file.name, 'rb') as data:
        request = {
            'username': 'testuser',
            'email': 'stepik@stepik.stepik',
            'image': data,
        }
        request.pop(dict_key)
        got = api.post('/api/v1/works/', request, format='multipart', expected_status_code=400)

    assert not Work.objects.exists()
    assert not WorkImage.objects.exists()
    assert got[dict_key] == ['This field is required.']


def test_work_creation_without_image_must_fail(api, image):
    got = api.post('/api/v1/works/', {
        'username': 'testuser',
        'email': 'stepik@stepik.stepik',
    }, format='multipart', expected_status_code=400)

    assert not Work.objects.exists()
    assert not WorkImage.objects.exists()
    assert got['image'] == ['New work should contain at least one image file in post body']
