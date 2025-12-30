from rest_framework import serializers

from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["id", "cart", "product", "quantity"]
        read_only_fields = ["id"]


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer

    class Meta:
        model = Cart
        fields = ["id", "products", "created_by", "created_at"]
        read_only_fields = ["id", "created_by"]
