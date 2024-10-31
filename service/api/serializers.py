"""
Модуль, описыващий DRF сериализаторы для API.
"""

from typing import Optional
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
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

    town = serializers.SerializerMethodField()

    class Meta:
        model = Street
        fields = ["name", "town"]

    @extend_schema_field(str)
    def get_town(self, obj) -> Optional[str]:
        """
        Получение названия города (вместо id).
        """
        return obj.town.name if obj.town else None


class ShopSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запроса списка магазинов.
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

    @extend_schema_field(str)
    def get_town(self, obj) -> Optional[str]:
        """
        Получение названия города (вместо id).
        """
        return obj.town.name if obj.town else None

    @extend_schema_field(str)
    def get_street(self, obj) -> Optional[str]:
        """
        Получение названия улицы (вместо id).
        """
        return obj.street.name if obj.street else None


class ShopCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания магазина.
    """

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
        extra_kwargs = {
            "street": {"required": True},
            "town": {"required": True},
        }
