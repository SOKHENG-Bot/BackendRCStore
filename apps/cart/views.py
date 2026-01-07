from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.views import Response
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action

from .models import Cart, CartProduct
from .serializers import (AddProductSerializer, CartProductSerializer,
                          CartSerializer)


class CartViewSet(viewsets.ModelViewSet):
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
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            cart_product, created = CartProduct.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={"quantity": quantity},
            )

            if not created:
                cart_product.quantity += quantity
                cart_product.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        cart = Cart.objects.get(created_by=request.user)
        product_id = serializer.validated_data["product_id"]
        cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)

        return_serializer = CartProductSerializer(cart_product)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["delete", "get"])
    def clear(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        if request.method == "GET":
            cart_product = CartProduct.objects.filter(cart=cart).select_related(
                "product"
            )
            serializer = self.get_serializer(cart_product, many=True)
            return Response(serializer.data)

        elif request.method == "DELETE":
            cart.cart_products.all().delete()
            # Also remove cart object
            if not cart.cart_products.exists():
                cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
