from rest_framework import serializers
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    # Nested product object data from Order Product
    product = OrderProductSerializer(many=True, read_only=True)
    ordered_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "ordered_by",
            "total",
            "status",
            "created_at",
            "updated_at",
            "product",
        ]
