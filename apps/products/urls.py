from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"categories", views.CategoryViewSet, basename="categories")

urlpatterns = router.urls
