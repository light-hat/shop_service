"""
Модуль, описыващий DRF сериализаторы для API.
"""

from typing import Optional

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для города.
    """

    class Meta:
        """Метаданные сериализатора."""

        model = City
        fields = ["id", "name"]


class StreetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для улицы.
    """

    city = serializers.SerializerMethodField()

    class Meta:
        """Метаданные сериализатора."""

        model = Street
        fields = ["id", "name", "city"]

    @extend_schema_field(str)
    def get_city(self, obj) -> Optional[str]:
        """
        Получение названия города (вместо id).
        """
        return obj.city.name if obj.city else None


class ShopSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запроса списка магазинов.
    """

    city = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()

    class Meta:
        """Метаданные сериализатора."""

        model = Shop
        fields = [
            "name",
            "city",
            "street",
            "house",
            "opening_time",
            "closing_time",
        ]

    @extend_schema_field(str)
    def get_city(self, obj) -> Optional[str]:
        """
        Получение названия города (вместо id).
        """
        return obj.city.name if obj.city else None

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
        """Метаданные сериализатора."""

        model = Shop
        fields = [
            "name",
            "city",
            "street",
            "house",
            "opening_time",
            "closing_time",
        ]
        extra_kwargs = {
            "street": {"required": True},
            "city": {"required": True},
        }
