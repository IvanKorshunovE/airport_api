from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from orders.models import Order
from orders.serializers import OrderListSerializer, OrderCreateSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = (
        Order.objects
        .prefetch_related(
            "tickets__flight__route__source",
            "tickets__flight__route__destination",
        )
        .all()
    )
    pagination_class = OrderPagination
    # permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return Order.objects.filter(user=self.request.user)
    #
    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
