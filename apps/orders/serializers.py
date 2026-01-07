from rest_framework import serializers

from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ["id", "order", "price", "product", "quantity"]
        read_only_fields = ["order", "price", "quantity", "product"]


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    ordered_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "ordered_by", "status", "order_products"]
        read_only_fields = ["id", "ordered_by", "created_at", "updated_at"]
