from django.db import transaction
from drf_yasg.views import Response
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action

from .models import Cart, CartProduct
from .serializers import (AddProductSerializer, CartProductSerializer,
                          CartSerializer)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Cart.objects.filter(created_by=self.request.user)


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return CartProduct.objects.filter(cart__created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return AddProductSerializer
        return CartProductSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(created_by=self.request.user)
            serializer.save(cart=cart)

    @action(detail=False, methods=["delete", "get"])
    def clear(self, request):
        cart_product = CartProduct.objects.filter(cart__created_by=self.request.user)

        if request.method == "GET":
            serializer = self.get_serializer(cart_product, many=True)
            return Response(serializer.data)

        elif request.method == "DELETE":
            cart_product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
