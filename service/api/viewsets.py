"""
Модуль, описывающий логику обработки API-запросов.
"""

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django.utils.timezone import now
from django.db.models import Case, When, BooleanField
from .models import Town, Street, Shop
from .serializers import (
    TownSerializer,
    StreetSerializer,
    ShopSerializer,
    ShopCreateSerializer,
)


class TownViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Описывает логику обработки запросов для городов.
    """

    queryset = Town.objects.all()
    serializer_class = TownSerializer
    http_method_names = ["get", "post"]

    @extend_schema(
        responses=StreetSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="street")
    def street_list(self, request, pk=None):
        """Получение списка всех улиц в указанном городе по ID города"""
        streets = Street.objects.filter(town_id=pk)

        page = self.paginate_queryset(streets)
        if page is not None:
            serializer = StreetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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

    def get_serializer_class(self):
        """
        Выбор сериализатора, для POST-запроса используется свой.
        """
        if self.action == "create":
            return ShopCreateSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "street",
                type={"type": "array", "items": {"type": "integer"}},
                description="Список ID улиц для фильтрации, например: street=1,2,3",
                style="form",
                explode=False,
            ),
            OpenApiParameter("city", OpenApiTypes.INT, description="ID города"),
            OpenApiParameter(
                "open",
                OpenApiTypes.INT,
                description="1 - открытые магазины, 0 - закрытые",
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

        street_ids = request.query_params.get("street")
        if street_ids:
            # Преобразуем строку "1,2" в список [1, 2]
            try:
                street_ids = [int(id) for id in street_ids.split(",")]
                queryset = queryset.filter(street_id__in=street_ids)
            except ValueError:
                return Response(
                    {
                        "error": "Invalid format for street IDs. Expected comma-separated integers."
                    },
                    status=400,
                )

        city_id = request.query_params.get("city")
        if city_id:
            queryset = queryset.filter(town_id=city_id)

        current_time = now().time()
        queryset = queryset.annotate(
            is_open=Case(
                When(
                    opening_time__lte=current_time,
                    closing_time__gte=current_time,
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            )
        )

        is_open = request.query_params.get("open")
        if is_open is not None:
            if is_open == "1":
                queryset = queryset.filter(is_open=True)
            else:
                queryset = queryset.filter(is_open=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ShopCreateSerializer, responses={"200": ShopCreateSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Определяет логику обработки POST-запроса на создание магазина.
        Возвращает объект ответа с кодом 200 и объект магазина.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
