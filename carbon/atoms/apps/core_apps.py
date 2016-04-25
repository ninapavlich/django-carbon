from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
    name = settings.CORE_APP

    def ready(self):
        import carbon.compounds.core.signals.handlers