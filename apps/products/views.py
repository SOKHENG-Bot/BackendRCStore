from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from .models import Category, Product
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    search_fields = ["name"]
    filterset_fields = ["name"]
    ordering_fields = ["created_at"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    @swagger_auto_schema(request_body=CategorySerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path="products")
    def get_products(self, request, pk=None):
        try:
            category = self.get_object()
            products = Product.objects.filter(category=category)

            page = self.paginate_queryset(products)
            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"Error": "Category not found"}, status=404)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    search_fields = ["name", "description"]
    filterset_fields = ["category", "price"]
    ordering_fields = ["price", "created_at"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    @swagger_auto_schema(request_body=ProductSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
