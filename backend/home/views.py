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
        data = {
            'category_list': serializer.data,
            'catalog_url': f'{settings.SITE_URL}/shop/',
            'accaunts_url' : f'None',
            'cart_url' : f'None',
            'contats_url' :f'None',
        }
        return Response(data)
