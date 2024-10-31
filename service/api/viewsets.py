"""
Модуль, описывающий логику обработки API-запросов.
"""

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils.timezone import now
from .models import Town, Street, Shop
from .serializers import TownSerializer, StreetSerializer, ShopSerializer


class TownViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Описывает логику обработки запросов для городов.
    """

    queryset = Town.objects.all()
    serializer_class = TownSerializer
    http_method_names = ["get", "post"]

    @extend_schema(
        responses=StreetSerializer(many=True),
        parameters=[OpenApiParameter("city_id", int, description="ID города")],
    )
    @action(detail=True, methods=["get"], url_path="street")
    def street_list(self, request):
        """Получение списка всех улиц в указанном городе по ID города"""
        try:
            town = self.get_object()
        except Town.DoesNotExist:
            return Response({"error": "Город не найден"}, status=400)

        streets = Street.objects.filter(town=town)
        serializer = StreetSerializer(streets, many=True)

        return Response(serializer.data)


# viewsets.ModelViewSet
class ShopViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Описывает логику обработки запросов для магазинов.
    """

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    http_method_names = ["get", "post"]

    @extend_schema(
        parameters=[
            OpenApiParameter("street", int, description="ID улицы"),
            OpenApiParameter("city", int, description="ID города"),
            OpenApiParameter(
                "open", int, description="1 - открытые магазины, 0 - закрытые"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Определяет логику обработки GET-запроса на получение списка магазинов.
        Возвращает объект ответа с кодом 200 и списком магазинов,
        либо с кодом 400 и сообщением об ошибке.
        """
        queryset = self.filter_queryset(self.get_queryset())

        street_id = request.query_params.get("street")
        city_id = request.query_params.get("city")
        is_open = request.query_params.get("open")

        if street_id:
            queryset = queryset.filter(street_id=street_id)
        if city_id:
            queryset = queryset.filter(town_id=city_id)
        if is_open is not None:
            current_time = now().time()
            if is_open == "1":
                queryset = queryset.filter(
                    opening_time__lte=current_time, closing_time__gte=current_time
                )
            else:
                queryset = queryset.exclude(
                    opening_time__lte=current_time, closing_time__gte=current_time
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=ShopSerializer, responses={"200": ShopSerializer})
    def create(self, request, *args, **kwargs):
        """
        Определяет логику обработки POST-запроса на создание магазина.
        Возвращает объект ответа с кодом 200 и объект магазина.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop = serializer.save()
        return Response({"id": shop.id}, status=status.HTTP_200_OK)
