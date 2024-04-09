from rest_framework import viewsets, status
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from shop.models import Category, Product
from cart.models import Cart, CartItem
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer
from shop.pagination import StandardResultsSetPagination
from django.utils.decorators import method_decorator
from config.cache import cache_heavy_get_requests

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    @method_decorator(cache_heavy_get_requests(timeout=86400))
    @action(detail=False, methods=['get'], url_path='detail/(?P<slug>[-\w]+)', url_name='product_detail')
    def product_detail(self, request, slug=None):
        """
        Генерит ссылку на детали продукта
        """
        product = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @method_decorator(cache_heavy_get_requests(timeout=86400))
    @action(detail=False, methods=['get'], url_path='filtered', url_name='filtered')
    def filtered(self, request):
        """
        Фильтры для характеристик товара
        """
        filter_params = request.query_params.dict()
        characteristics_filter = {k: v for k, v in filter_params.items() if "characteristics__" in k}
        simple_filter_params = {k: v for k, v in filter_params.items() if "characteristics__" not in k}

        order_param = simple_filter_params.pop('order', None)
        
        filtered_queryset = self.queryset.filter(**simple_filter_params)
    
        for param, value in characteristics_filter.items():
            json_field = param.split('__', 1)[1]  
            filtered_queryset = filtered_queryset.filter(**{f'characteristics__{json_field}': value})

        if order_param:
            if order_param == 'price_asc':
                filtered_queryset = filtered_queryset.order_by('price')
            elif order_param == 'price_desc':
                filtered_queryset = filtered_queryset.order_by('-price') # потом можно сюда засунуть другие параметры фильтрации, когда сбор куки подключу
         
        try:
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='add-to-cart', url_name='add_to_cart')
    def add_to_cart(self, request, pk=None):
        """
        Добавляет в корзину товар
        """
        product = get_object_or_404(self.get_queryset(), pk=pk)
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Аутентификация необходима'}, status=status.HTTP_403_FORBIDDEN)

        cart, _ = Cart.objects.get_or_create(user=user)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_200_OK)

    @method_decorator(cache_heavy_get_requests(timeout=86400))
    @action(detail = False, methods = ['get'], url_path = 'search', url_name = 'search')
    def search(self, request):
        """
        Поисковик товара (ключевые слова в категориях, названии товара ии его характеристиках)
        """
        query = request.query_params.get('q', None)

        if query is None:
            return Response({'error' : 'Отсуствует поисковой запрос'}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(characteristics__icontains=query)

        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
