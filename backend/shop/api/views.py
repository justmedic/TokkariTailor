from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from shop.models import Category, Product
from cart.models import Cart, CartItem
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


    @action(detail=False, methods=['get'], url_path='detail/(?P<slug>[-\w]+)', url_name='product_detail')
    def product_detail(self, request, slug=None):
        product = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.get_serializer(product)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='filtered', url_name='filtered')
    def filtered(self, request):
        filter_params = request.query_params.dict()
        characteristics_filter = {k: v for k, v in filter_params.items() if "characteristics__" in k}
        simple_filter_params = {k: v for k, v in filter_params.items() if "characteristics__" not in k}
        
        filtered_queryset = self.queryset.filter(**simple_filter_params)
    
        for param, value in characteristics_filter.items():
            json_field = param.split('__', 1)[1]  
            filtered_queryset = filtered_queryset.filter(**{f'characteristics__{json_field}': value})
            
        try:
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='add-to-cart', url_name='add_to_cart')
    def add_to_cart(self, request, pk=None):
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

