from django.conf import settings
from django.db import models

from apps.products.models import Product


class Cart(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"The cart created by {self.created_by} at {self.created_at}"

    @property
    def total_price(self):
        return sum(product.total_price for product in self.products.all())


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"This {self.cart} have product {self.product} {self.quantity} quantity"

    @property
    def total_price(self):
        return self.quantity * self.product.price
