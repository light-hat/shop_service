"""
Модуль конфигурации админ-панели для сервиса.
"""

from django.contrib import admin
from .models import Town, Street, Shop

admin.site.site_title = "Сервис магазинов"
admin.site.site_header = "Админка сервиса магазинов"
admin.site.index_title = "Админка"


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Town.
    """

    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Street.
    """

    list_display = ("name", "town")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("town",)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Shop.
    """

    list_display = ("name", "town", "street", "house", "opening_time", "closing_time")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("town",)
