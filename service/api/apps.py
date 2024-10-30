"""
Django-приложение для сервиса магазинов.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Конфигурация Django-приложения для сервиса магазинов.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
