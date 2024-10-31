"""
Модуль, описывающий модели БД сервиса.
"""

from django.db import models


class City(models.Model):
    """Модель, описывающая город."""

    name = models.CharField(max_length=100, verbose_name="Название города")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Street(models.Model):
    """Модель, описывающая улицу."""

    name = models.CharField(max_length=100, verbose_name="Название улицы")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Улица"
        verbose_name_plural = "Улицы"


class Shop(models.Model):
    """Модель, описывающая магазин."""

    name = models.CharField(max_length=100, verbose_name="Название магазина")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    street = models.ForeignKey(Street, on_delete=models.CASCADE, verbose_name="Улица")
    house = models.CharField(max_length=10, verbose_name="Дом")
    opening_time = models.TimeField(verbose_name="Время открытия")
    closing_time = models.TimeField(verbose_name="Время закрытия")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
