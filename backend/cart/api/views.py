from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer
from django.db import transaction

from shop.api.serializers import ProductSerializer



class CartViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт, который позволяет просматривать или редактировать корзины.
    
    Требуется аутентификация.
    Возвращает список всех корзин для текущего зарегистрированного пользователя.
    Позволяет создать новую корзину для аутентифицированного пользователя.

    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        """
        Этот метод возвращает список всех корзин для текущего пользователя.
        """
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Создает новую корзину для пользователя.
        """
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(user=self.request.user)



class CartItemViewSet(viewsets.ModelViewSet):
    """

    API для просмотра, создания и редактирования товаров в корзине.
    
    Требуется аутентификация.
    Возвращает элементы для корзины текущего пользователя.
    Позволяет добавлять элементы в корзину пользователя.

    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Этот метод возвращает список всех элементов в корзине для текущего пользователя.
        """
        user_cart = Cart.objects.filter(user=self.request.user)
        return CartItem.objects.filter(cart__in=user_cart)
   

    
    def perform_create(self, serializer):
        """

        Добавляет продукт в корзину пользователя или обновляет количество, если элемент уже существует.
        Гарантирует, что элемент корзины связан с активной корзиной пользователя.

        """
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        serializer.instance = cart_item
   
    @action(detail=False, methods=['post'], url_path='create_order', url_name='create_order')
    def create_order(self, request, *args, **kwargs):
        """

        Создает заказ из элементов, находящихся в корзине пользователя.
        
        Если корзина пуста, то возвращается ошибка 400 с сообщением.
        Если заказ успешно создан, возвращает ответ со ссылкой на заказ.

        """
        user = request.user
        user_cart = Cart.objects.filter(user=user)
        cart_items = CartItem.objects.filter(cart__in=user_cart)
        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_cost = 0
        product_info_list = []

        for item in cart_items:

            # это вот все нужно шобы оно выдавало полную ссылку на товар
            serializer = ProductSerializer(item.product, context={'request': request})
            product_url = serializer.get_product_url(item.product)

            total_cost += item.quantity * item.product.price
            product_characteristics = item.product.characteristics if item.product.characteristics else "Характеристики продукта не указаны."
            product_info_list.append({
                'Товар': item.product.name,
                'Ссылка' : product_url,
                'Количество': item.quantity,
                'Цена за единицу': item.product.price,
                'Характеристики': product_characteristics,
            })
    
        with transaction.atomic():
            order = Order.objects.create(user=user, total_cost=total_cost)
            order.items.set(cart_items)
            for item in cart_items:
                item.cart.is_active = False
                item.cart.save()
                item.save()
        
        print(f'product_info_list: {product_info_list}\n user:{user}\n user_phone:{user.phone}\nOrder_id: {order.id}') # заменить это говно на отправку инфы на сервер
                

        return Response({'message': 'Order has been created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)

