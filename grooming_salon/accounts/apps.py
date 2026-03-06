from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grooming_salon.accounts'

    # Uključujemo Django signal za kreiranje praznog profila
    def ready(self):
        import grooming_salon.accounts.signals
