from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.products.models import Product

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("delivering", "Delivery"),
    ("completed", "Completed"),
]


class Order(models.Model):
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.ordered_by


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "OrderProduct"
        verbose_name_plural = "OrderProducts"

    def __str__(self):
        return self.order
