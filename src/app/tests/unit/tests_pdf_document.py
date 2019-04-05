import mimetypes

import pytest
from django.test import override_settings

from app.pdf import PDFDocument


@pytest.fixture
def document():
    with override_settings(ABSOLUTE_HOST='https://hst.com/'):
        return PDFDocument(template_name='pdf/boilerplate.html')


def test_rendering(document):
    got = document.render_html()
    assert 'html' in got


def test_default_context(document):
    got = document.render_html()
    assert '<base href="https://hst.com/" />' in got


def test_additional_context():
    document = PDFDocument(template_name='pdf/boilerplate.html', spam='HAM')
    assert document.ctx['spam'] == 'HAM'


def test_rendering_pdf(document):
    got = document.render_pdf()
    assert len(got) > 500
