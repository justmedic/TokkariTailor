from django.db.models import Q
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

    @action(detail=False, methods=['get'], url_path='filtered', url_name='filtered')
    def filtered(self, request):
        filter_params = request.query_params.dict()
        characteristics_filter = {k: v for k, v in filter_params.items() if "characteristics__" in k}
        simple_filter_params = {k: v for k, v in filter_params.items() if "characteristics__" not in k}
        
        # Формируем базовый queryset
        filtered_queryset = self.queryset.filter(**simple_filter_params)
    
        for param, value in characteristics_filter.items():
            json_field = param.split('__', 1)[1]  
            filtered_queryset = filtered_queryset.filter(**{f'characteristics__{json_field}': value})
        try:
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

