from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
# from cloudinary_storage.storage import MediaCloudinaryStorage
# from core.utils import get_upload_path


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    slug = models.SlugField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(
        # upload_to=menu_image_upload_path,
        # storage=MediaCloudinaryStorage(),
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "products"

    def __str__(self):
        return self.name
