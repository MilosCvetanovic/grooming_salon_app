from django.apps import AppConfig


class NotificationsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grooming_salon.notifications_api'

    def ready(self):
        import grooming_salon.notifications_api.signals