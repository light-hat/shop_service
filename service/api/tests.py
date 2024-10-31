"""
Модуль, описывающий модульные тесты сервиса.
"""

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from .viewsets import ShopViewSet
from .models import City, Street, Shop
from .serializers import ShopCreateSerializer


@pytest.mark.django_db
def test_shop_creation_with_required_fields():
    """Тест на успешное создание объекта Shop с обязательными полями"""
    city = City.objects.create(name="Sample City")
    street = Street.objects.create(name="Sample Street", city=city)
    shop = Shop.objects.create(
        name="Test Shop",
        city=city,
        street=street,
        house="123",
        opening_time="09:00:00",
        closing_time="18:00:00",
    )
    assert shop.id is not None  # Проверяем, что объект создан в базе данных
    assert shop.name == "Test Shop"
    assert shop.city == city
    assert shop.street == street


@pytest.mark.django_db
def test_shop_create_serializer_valid_data():
    """
    Модульное тестирование сериализатора POST-запросов для магазина.
    Тестируем корректные данные.
    """
    city = City.objects.create(name="Sample City")
    street = Street.objects.create(name="Sample Street", city=city)

    # Тестируем корректные данные
    valid_data = {
        "name": "New Shop",
        "city": city.id,
        "street": street.id,
        "house": "789",
        "opening_time": "08:00:00",
        "closing_time": "22:00:00",
    }
    serializer = ShopCreateSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors  # Проверяем, что данные валидны


@pytest.mark.django_db
def test_shop_create_serializer_invalid_data():
    """
    Модульное тестирование сериализатора POST-запросов для магазина.
    Тестируем некорректные данные без обязательного поля street и с пустым значением city.
    """
    invalid_data = {
        "name": "New Shop",
        "house": "789",
        "opening_time": "08:00:00",
        "closing_time": "22:00:00",
        "city": None,  # Некорректное значение city
    }
    serializer = ShopCreateSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_shop_viewset_filtering():
    """
    Модульное тестирование представления для списка магазинов.
    Тестируем фильтрацию по улице.
    """
    city = City.objects.create(name="Sample City")
    street1 = Street.objects.create(name="Sample Street 1", city=city)
    street2 = Street.objects.create(name="Sample Street 2", city=city)
    Shop.objects.create(
        name="Shop 1",
        city=city,
        street=street1,
        house="123",
        opening_time="09:00:00",
        closing_time="18:00:00",
    )
    Shop.objects.create(
        name="Shop 2",
        city=city,
        street=street2,
        house="456",
        opening_time="10:00:00",
        closing_time="20:00:00",
    )

    factory = APIRequestFactory()
    view = ShopViewSet.as_view({"get": "list"})

    request = factory.get("/shop/", {"street": f"{street1.id}"})
    response = view(request)

    assert response.status_code == 200
    data = response.data.get("results", response.data)
    assert len(data) == 1
    assert data[0]["name"] == "Shop 1"
