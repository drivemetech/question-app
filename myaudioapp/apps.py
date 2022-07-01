from django.apps import AppConfig


class MyaudioappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myaudioapp'

    def ready(self):        
        from . import signals  # noqa
        