from rest_framework import serializers

from apps.products.serializers import ProductSerializer

from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "total_price"]
        read_only_fields = ["id"]


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(read_only=True, many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "total_price", "created_by", "cart_products"]
        read_only_fields = ["id", "created_by"]


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
