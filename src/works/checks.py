import subprocess
from shutil import which

from django.core.checks import Error, Tags, Warning, register

REQUIRED_WKHTMLTOPDF_VERSION = 'wkhtmltopdf 0.12.3 (with patched qt)'


@register(Tags.compatibility)
def check_wkhtmltopdf(app_configs=None, **kwargs):
    wxhtmltopdf_path = which('wkhtmltopdf')
    if wxhtmltopdf_path is None:
        return [
            Warning(
                'wkhtmltopdf binary is not found in $PATH',
                hint='If you need PDF printing, take a look at https://github.com/JazzCore/python-pdfkit#installation',
            ),
        ]

    version = subprocess.check_output([wxhtmltopdf_path, '--version']).decode('utf-8').strip()
    if version != REQUIRED_WKHTMLTOPDF_VERSION:
        return [
            Error(
                f'Wrong version of wkhtmltopdf(«{version}» instead of required «{REQUIRED_WKHTMLTOPDF_VERSION}»)',
                hint='Install the official (not your distro) version from https://wkhtmltopdf.org/downloads.html',
            ),
        ]

    return []
