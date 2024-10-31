"""
Модуль, описыващий DRF сериализаторы для API.
"""

from rest_framework import serializers
from .models import Town, Street, Shop


class TownSerializer(serializers.ModelSerializer):
    """
    Сериализатор для города.
    """

    class Meta:
        model = Town
        fields = ["name"]


class StreetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для улицы.
    """

    class Meta:
        model = Street
        fields = ["name", "town"]


class ShopSerializer(serializers.ModelSerializer):
    """
    Сериализатор для магазина.
    """

    town = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            "name",
            "town",
            "street",
            "house",
            "opening_time",
            "closing_time",
        ]

    def get_town(self, obj):
        """
        Получение названия города (вместо id).
        """
        return obj.town.name if obj.town else None

    def get_street(self, obj):
        """
        Получение названия улицы (вместо id).
        """
        return obj.street.name if obj.street else None
