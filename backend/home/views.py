from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from shop.models import Category  
from shop.api.serializers import CategorySerializer  

class HomeAPIView(APIView):
    """
    API представление для домашней страницы.
    """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, context={'request': request}, many=True)
        
        is_authenticated = request.user.is_authenticated

        data = {
            'category_list': serializer.data,
            'catalog_url': f'{settings.SITE_URL}/shop/',
            'user_reg' : f'{settings.SITE_URL}/accounts/user/register',
            'user_log' : f'{settings.SITE_URL}/accounts/user/login',
            'user_logount' : f'{settings.SITE_URL}/accounts/user/logout_user',
            'cart_url' : f'{settings.SITE_URL}/cart/user_cart/',
            'search_url': f'{settings.SITE_URL}/products/search/',
            'contats_url' :f'None',
            'is_authenticated': is_authenticated
        }
        if is_authenticated:
            data['username'] = request.user.username
        return Response(data)
