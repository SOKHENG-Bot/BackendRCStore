from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(request_body=CartSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="/add")
    def add_product(self, request, pk=None):
        cart = self.get_object()
        product = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            cart.add_product(product, quantity)
            cart.save()
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
