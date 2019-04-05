import uuid

import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template import loader


class PDFDocument:
    """
    A document that gets template name and renders it to PDF

    Your template will have no app-wide context, sorry

    Examples:
        r = PDFDocument(
            tempalte_name='orders/pdf/client.html',
            object'=Order.objects.get(pk=12),
        )

        r.render_pdf()  # render PDF, returnes bytes
        r.render_html()  # render HTML, returnes string

    """
    PDFKIT_OPTIONS = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }

    def __init__(self, template_name: str, **ctx):
        self.template_name = template_name

        self.ctx = ctx
        self.ctx.update(
            self.get_context_data(),
        )

        self.template = loader.get_template(self.template_name)

    def get_context_data(self) -> dict:
        return dict(
            ABSOLUTE_HOST=settings.ABSOLUTE_HOST,
        )

    def get_pdfkit_options(self) -> dict:
        return self.PDFKIT_OPTIONS

    def render_html(self) -> str:
        return self.template.render(self.ctx)

    def render_pdf(self) -> bytes:
        html = self.render_html()

        options = self.get_pdfkit_options()
        return pdfkit.from_string(html, False, options)

    def get_filename(self) -> str:
        return str(uuid.uuid4()) + '.pdf'


class PDFViewMixin:
    """
    A view that renderes PDF from given template_name.

    """
    template_name = None
    document_class = PDFDocument

    def get(self, request, *args, **kwargs) -> HttpResponse:
        ctx = self.get_context_data()
        self.document = self.document_class(template_name=self.template_name, **ctx)

        if 'html' in request.GET.keys():  # return plain HTML
            return HttpResponse(self.document.render_html())

        pdf = self.document.render_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')

        if 'inline' not in request.GET.keys():
            response['Content-Disposition'] = 'attachment; filename=%s' % self.document.get_filename()

        response['Content-Length'] = len(pdf)
        return response

    def get_context_data(self) -> dict:
        return dict()
