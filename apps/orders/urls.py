from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"orders", views.OrderViewSet, basename="orders")
router.register(r"order-product", views.OrderProductViewSet, basename="order_product")
urlpatterns = router.urls
