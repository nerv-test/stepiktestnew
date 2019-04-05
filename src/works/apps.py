from django.apps import AppConfig


class WorkConfig(AppConfig):
    name = 'works'

    def ready(self):
        import works.checks  # noqa

        import works.signals.handlers  # noqa
