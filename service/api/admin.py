"""
Модуль конфигурации админ-панели для сервиса.
"""

from django.contrib import admin
from .models import City, Street, Shop

admin.site.site_title = "Сервис магазинов"
admin.site.site_header = "Админка сервиса магазинов"
admin.site.index_title = "Админка"


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели City.
    """

    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Street.
    """

    list_display = ("name", "city")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("city",)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Shop.
    """

    list_display = ("name", "city", "street", "house", "opening_time", "closing_time")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("city",)
