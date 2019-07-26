from django.apps import AppConfig


class InceptionConfig(AppConfig):
    name = 'inception'

    def ready(self):
        from inception.signals import run_spider, delete_image
