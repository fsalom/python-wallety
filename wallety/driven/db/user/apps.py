# driven/db/user/apps.py
from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'driven.db.user'
    label = 'user'
    default_auto_field = "django.db.models.BigAutoField"
