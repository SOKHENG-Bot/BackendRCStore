from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import Response, status

from apps.cart import serializers
from apps.products.models import Product

from .models import Cart, CartProduct
from .serializers import (AddProductSerializer, CartProductSerializer,
                          CartSerializer, UpdateProductSerializer)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Cart.objects.filter(created_by=self.request.user)

    @action(detail=False, methods=["post"], serializer_class=AddProductSerializer)
    def add_product(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = Cart.objects.get_or_create(created_by=request.user)

        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product with query ID not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity = serializer.validated_data["quantity"]
        product = get_object_or_404(Product, id=product_id)

        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_product.quantity += quantity
            cart_product.cart.save()

        return_serializer = CartSerializer(cart)
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=["get", "put"], serializer_class=UpdateProductSerializer
    )
    def update_product(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_product = get_object_or_404(CartProduct, product_id=product_id, cart=cart)

        if request.method == "GET":
            serializer = CartProductSerializer(cart_product)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = UpdateProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            cart_product.quantity = serializer.validated_data["quantity"]
            cart_product.save()

            cart_serializer = CartProductSerializer(cart_product)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "delete"])
    def remove_product(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_product = get_object_or_404(CartProduct, product_id=product_id, cart=cart)

        if request.method == "GET":
            serializer = CartProductSerializer(cart_product)
            return Response(serializer.data)

        elif request.method == "DELETE":
            cart_product.delete()
            return Response(
                {"detail": "Product have remove from cart."},
                status=status.HTTP_200_OK,
            )

    # Function to clear all product from cart
    @action(detail=False, methods=["get", "delete"])
    def clear_cart(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        if request.method == "GET":
            serializer = CartSerializer(cart)
            return Response(serializer.data)

        elif request.method == "DELETE":
            CartProduct.objects.filter(cart=cart).delete()
            return Response({"detail": "Cart have clean successful."})

    # Function to remove cart
    @action(detail=False, methods=["get", "delete"])
    def remove_cart(self, request):
        cart = get_object_or_404(Cart, created_by=request.user)

        if request.method == "GET":
            serializer = CartSerializer(cart)
            return Response(serializer.data)

        elif request.method == "DELETE":
            cart.delete()
            return Response({"detail": "Cart have delete successful."})
