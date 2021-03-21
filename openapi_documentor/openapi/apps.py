from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OpenapiConfig(AppConfig):
    name = "openapi_documentor.openapi"
    verbose_name = _("Openapi")

    def ready(self):
        try:
            import openapi_documentor.openapi.signals  # noqa F401
        except ImportError:
            pass
