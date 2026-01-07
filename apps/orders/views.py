from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response

from apps.cart.models import Cart

from .models import Order, OrderProduct
from .serializers import OrderProductSerializer, OrderSerializer


class RetrieveUpdateDestroyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides `retrieve`, `update`, and `destroy` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    pass


class OrderViewSet(RetrieveUpdateDestroyViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["status"]

    def get_queryset(self):
        return Order.objects.filter(ordered_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        return OrderProduct.objects.filter(order__ordered_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        with transaction.atomic():
            cart = get_object_or_404(Cart, created_by=self.request.user)
            if not cart.cart_products.exists():
                return Response({"error": "Cart is empty"})

            order = Order.objects.create(
                ordered_by=self.request.user,
                status="pending",
            )

            for item in cart.cart_products.all():
                OrderProduct.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            cart.cart_products.all().delete()
            if not cart.cart_products.exists():
                cart.delete()
