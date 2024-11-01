"""
Модуль, описывающий логику обработки API-запросов.
"""

from django.db.models import BooleanField, Case, When
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import City, Shop, Street
from .serializers import (
    CitySerializer,
    ShopCreateSerializer,
    ShopSerializer,
    StreetSerializer,
)


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Описывает логику обработки запросов для городов.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ["get", "post"]

    @extend_schema(
        responses=StreetSerializer(many=True),
    )
    @action(detail=True, methods=["get"], url_path="street")
    def street_list(self, request, pk=None):
        """Получение списка всех улиц в указанном городе по ID города"""
        try:
            filtered_streets = Street.objects.select_related("city").filter(city_id=pk)

            page = self.paginate_queryset(filtered_streets)
            if page is not None:
                serializer = StreetSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = StreetSerializer(filtered_streets, many=True)

            return Response(serializer.data)

        except (ValidationError, ValueError) as e:
            return Response(
                {
                    "error": str(e),
                },
                status=400,
            )


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
        try:
            queryset = self.filter_queryset(self.get_queryset())

            street_ids = request.query_params.get("street")
            if street_ids:
                # Преобразуем входную строку "1,2" в список [1, 2]
                try:
                    street_ids = list(map(int, street_ids.split(",")))
                    queryset = queryset.filter(street_id__in=street_ids)
                except (ValidationError, ValueError):
                    return Response(
                        {"error": "Некорректный формат идентификаторов улиц."},
                        status=400,
                    )

            city_id = request.query_params.get("city")
            if city_id:
                queryset = queryset.filter(city_id=city_id)

            # Аннотируем поле is_open в queryset.
            # Работает как if/else, только в SQL (CASE WHEN ... THEN ... ELSE ... END).
            current_time = timezone.localtime().time()
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
            # По аннотированному параметру фильтруем открытые, либо закрытые магазины.
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
        except (ValidationError, ValueError) as e:
            return Response(
                {
                    "error": str(e),
                },
                status=400,
            )

    @extend_schema(
        request=ShopCreateSerializer, responses={"200": ShopCreateSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Определяет логику обработки POST-запроса на создание магазина.
        Возвращает объект ответа с кодом 200 и объект магазина.
        """
        try:

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {
                    "error": str(e),
                },
                status=400,
            )
