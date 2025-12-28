from rest_framework import serializers
from .models import Cart, CartProduct


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "created_by", "created_at"]
        read_only_fiels = ["id", "created_by"]


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["id", "cart", "product", "quantity"]
        read_only_fields = ["id"]
