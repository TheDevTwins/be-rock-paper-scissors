from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "be_rock_paper_scissors.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import be_rock_paper_scissors.users.signals  # noqa F401
        except ImportError:
            pass
