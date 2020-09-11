from django.conf import settings
from rest_framework.settings import perform_import


class Settings:
    def __getattr__(self, attr):
        user_settings = getattr(settings, 'CHANNELS', {})
        val = perform_import(user_settings[attr], attr)
        return val


channels_settings = Settings()
