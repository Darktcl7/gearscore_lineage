from django.apps import AppConfig


class DkpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dkp'

    def ready(self):
        import dkp.signals  # noqa: F401
