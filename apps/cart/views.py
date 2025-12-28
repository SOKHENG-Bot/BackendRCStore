from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(request_body=CartSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
