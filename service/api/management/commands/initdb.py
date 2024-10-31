"""
Кастомная manage.py командп для инициализации системы при первом запуске.
"""

import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from api.models import City, Street, Shop


class Command(BaseCommand):
    """
    Команда для инициализации базы данных.
    """

    def handle(self, *args, **options):
        """Запуск действий команды."""

        cities = [
            "Москва",
            "Санкт-Петербург",
            "Нижний Новгород",
            "Казань",
            "Екатеринбург",
            "Новосибирск",
            "Челябинск",
            "Ростов-на-Дону",
            "Уфа",
            "Самара",
            "Омск",
            "Воронеж",
            "Красноярск",
            "Пермь",
            "Волгоград",
            "Пенза",
            "Саратов",
            "Тюмень",
            "Тольятти",
            "Ижевск",
            "Ульяновск",
            "Иркутск",
            "Ярославль",
            "Владивосток",
            "Донецк",
            "Севастополь",
            "Симферополь",
            "Луганск",
            "Грозный",
            "Краснодар",
        ]

        streets = [
            "Ленина",
            "Советская",
            "Октябрьская",
            "Комсомольская",
            "Кирова",
            "Мира",
            "Победы",
            "Свободы",
            "Труда",
            "Школьная",
            "Молодежная",
            "Ленина",
            "Советская",
            "Октябрьская",
            "Комсомольская",
            "Кирова",
            "Мира",
            "Победы",
            "Свободы",
            "Труда",
            "Школьная",
            "Молодежная",
            "Войкова",
            "Пушкина",
        ]

        houses = ["17", "2", "4", "48", "51", "6", "12", "8", "22", "10"]

        opening_times = [
            "5:00",
            "6:00",
            "7:00",
            "8:00",
            "9:00",
        ]

        closing_times = [
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
        ]

        shop_names = [
            "Пятерочка",
            "Магнит",
            "Дикси",
            "Ашан",
            "Лента",
            "Перекресток",
            "Wildberries",
            "Ozon",
            "Fix Price",
            "DNS",
        ]

        try:
            User.objects.get(username="admin")
            print("Администратор уже создан.")

        except User.DoesNotExist:
            User.objects.create_superuser(username="admin", password="admin")

        for city in cities:
            City.objects.get_or_create(name=city)

        for city_object in City.objects.all():
            Street.objects.get_or_create(name=random.choice(streets), city=city_object)

        streets_objects = Street.objects.all()

        for street in streets_objects:
            Shop.objects.get_or_create(
                name=random.choice(shop_names),
                city=street.city,
                street=street,
                house=random.choice(houses),
                opening_time=random.choice(opening_times),
                closing_time=random.choice(closing_times),
            )
