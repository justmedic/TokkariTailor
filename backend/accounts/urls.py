from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import UserViewSet


app_name = 'accounts' 


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]