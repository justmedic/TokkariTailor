from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Category, Product
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['post'], url_path='filtered')
    def filtered(self, request):
        filter_params = request.data  # Получаем фильтры из тела запроса в виде словаря
        try:
            filtered_queryset = self.queryset.filter(**filter_params)
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# class PrisuctListviews(APIView):
#     def get (self, request, category_id):
#         category = Category.objects.get(id = category_id)
#         product = Product.objects.filter(category = category)

#         available_filters = category.filters

#         for filter_key in available_filters.keys():
#             if filter_key in request.query_params:
#                 filters