from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Предполагается, что у вас есть view функция home_page_view

    ]