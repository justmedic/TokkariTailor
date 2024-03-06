from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'user_cart', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
