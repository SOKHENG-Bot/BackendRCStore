from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import Response

from apps.products.models import Product

from .models import Cart, CartProduct
from .serializers import (AddProductSerializer, CartProductSerializer,
                          CartSerializer, UpdateProductSerializer)


class CartViewSet(viewsets.ViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        cart = Cart.objects.filter(created_by=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="add",
        serializer_class=AddProductSerializer,
    )
    def add_product(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        if request.method == "GET":
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            serializer = AddProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]
            product = get_object_or_404(Product, id=product_id)
            cart_product, product_created = CartProduct.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": quantity}
            )

            if not product_created:
                cart_product.quantity += int(quantity)
                cart_product.save()

            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)

    @action(
        detail=True,
        methods=["get", "put"],
        url_path="update",
        serializer_class=UpdateProductSerializer,
    )
    def update_product(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk, created_by=request.user)
        product_id = request.query_params.get("product_id")
        cart_product = get_object_or_404(CartProduct, product_id=product_id, cart=cart)

        if request.method == "GET":
            serializer = CartProductSerializer(cart_product)
            return Response(serializer.data)
        else:
            serializer = UpdateProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            quantity = serializer.validated_data["quantity"]
            cart_product.quantity = quantity
            cart_product.save()
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)

    @action(detail=True, methods=["get", "delete"], url_path="remove")
    def remove_product(self, request, pk=None):
        cart = get_object_or_404(Cart, id=pk, created_by=request.user)
        cart_prodcut = get_object_or_404(CartProduct, id=pk, cart=cart)

        if request.method == "GET":
            serializer = CartProductSerializer(cart_prodcut)
            return Response(serializer.data)
        else:
            product_id = request.query_params.get("product_id")
            cart_prodcut = get_object_or_404(
                CartProduct, cart=cart, product_id=product_id
            )
            cart_prodcut = get_object_or_404(CartProduct, id=pk, cart=cart)
            cart_prodcut.delete()
            return Response({"detail": "Product removed from cart."})

    @action(detail=False, methods=["get", "delete"], url_path="clear")
    def clear_cart(self, request):
        if request.method == "GET":
            cart, _ = Cart.objects.get_or_create(created_by=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            cart = get_object_or_404(Cart, created_by=request.user)
            cart.delete()
            return Response({"detail": "Cart have cleared."})
