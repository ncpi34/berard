from django.apps import AppConfig


class FileIntegrationConfig(AppConfig):
    name = 'file_integration'

    # def ready(self):
    #     from forecastUpdater import update
    #     update.start()
