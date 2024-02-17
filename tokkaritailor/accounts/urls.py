from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from . import views 

app_name = 'accounts' 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True, next_page='/'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
