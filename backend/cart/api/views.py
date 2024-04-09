from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer
from django.db import transaction
import json
import requests
from django.shortcuts import get_object_or_404

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
        return CartItem.objects.filter(cart__user=self.request.user)
   

    
    def perform_create(self, serializer):
        """

        Добавляет продукт в корзину пользователя или обновляет количество, если элемент уже существует.
        Гарантирует, что элемент корзины связан с активной корзиной пользователя.

        """
        cart, __ = Cart.objects.get_or_create(user=self.request.user, defaults={'total_cost': 0})          # что это?  О_О  
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
        user=request.user
        user_cart = get_object_or_404(Cart, user= user)
        cart_items = user_cart.items.all()

        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_cost = get_object_or_404(Cart, user=user).get_total_cost()
        product_info_list = []

        for item in cart_items:
           
            # это вот все внизу нужно шобы оно выдавало полную ссылку на товар
            product_url = ProductSerializer(item.product, context={'request': request}).get_product_url(item.product)

            total_cost += item.quantity * item.product.price
            product_characteristics = item.product.characteristics if item.product.characteristics else "Характеристики продукта не указаны."
            product_info_list.append({
                'Товар': str(item.product.name),
                'Ссылка' : str(product_url),
                'Количество': str(item.quantity),
                'Цена за единицу': str(item.product.price),
                'Характеристики': str(product_characteristics),
            })

        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_cost=total_cost)
            order.items.set(cart_items)
            CartItem.objects.filter(cart=user_cart).delete()  # ? ля я хз это вообще будет работать или нет 
            user_cart.delete()
            
        order_data = {
            "order_id": order.id,
            "user" : user.username,
            "user_phone" : user.phone,
            "product_info_list" : product_info_list 
        }
        print(f'order_data = {order_data}')
        msg_response = requests.post("http://127.0.0.1:5111/order/", json = order_data )                
        if msg_response.status_code == 200:
            print(msg_response.json())
            return Response({'message': 'Order has been created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)

        else:
            print(f"Произошла ошибка. Код ответа: {msg_response.status_code}")
            return Response({'message': 'Error', 'order_id': order.id}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


