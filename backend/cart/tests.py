from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import CustomUser
from shop.models import Product, Category
from cart.models import Cart, CartItem, Order

from shop.api.serializers import ProductSerializer

class CartTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
        email='testemail@example.com',
        phone = '89991231234',
        username='testemail@example.com',
        password='testpassword123')
        self.client = APIClient()

        # Делаем запрос на логин для получения токена
        response = self.client.post('/accounts/user/login/', {
            'username': 'testemail@example.com',
            'password': 'testpassword123',
        })
        # print(response.data)
        self.token = response.data['token']  # Получаем токен из ответа
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category, name="Laptop", slug="laptop", 
            price=1000, stock=5, available=True, characteristics={})
        

        self.cart = Cart.objects.create(user=self.user)

    def test_add_item_to_cart(self):

        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        
        self.assertEqual(self.cart.items.count(), 1)
        self.assertTrue(self.cart.items.filter(product=self.product).exists())
        self.assertEqual(self.cart.items.get(product=self.product).quantity, 1)

        factory = APIRequestFactory() 
        request = factory.get('/')

        product_info = ProductSerializer(self.product, context={'request': request}).data
        # print("Информация о продукте, добавленном в корзину:")
        # print(product_info)

    def test_add_multiple_items_to_cart(self):

        product2 = Product.objects.create(
            category=self.category, name="Smartphone", slug="smartphone",
            price=500, stock=10, available=True, characteristics={})
        

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=self.cart, product=product2, quantity=2)
        

        self.assertEqual(self.cart.items.count(), 2)
        self.assertEqual(CartItem.objects.filter(cart=self.cart, product=product2).count(), 1)
        self.assertEqual(CartItem.objects.get(cart=self.cart, product=product2).quantity, 2)

    def test_create_order_with_empty_cart(self):
        """
        Тестирует попытку создания заказа с пустой корзиной.
        """
        url = reverse('cart:cartitem-create_order')

        response = self.client.post(url)
        # print(f'{response.data}\n')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Корзина пуста')

    def test_create_order_success(self):
        """
        Тестирует успешное создание заказа из элементов в корзине.
        """

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        
        url = reverse('cart:cartitem-create_order')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Order has been created successfully')
        self.assertIn('order_id', response.data)

        order_id = response.data['order_id']

        order = Order.objects.get(id=order_id)
        
        # print("Созданный заказ содержит следующие элементы:")
        # for item in order.items.all():
        #     product = item.product
        #     characteristics = product.characteristics 

        #     print(f"Товар: {product.name}, Количество: {item.quantity}, Цена за единицу: {product.price}")
        #     if characteristics:
        #         print("Характеристики продукта:")
        #         for key, value in characteristics.items():
        #             print(f"    {key}: {value}")
        #     else:
        #         print("    Характеристики продукта не указаны.")
        

        # print(f"Общая стоимость заказа: {order.total_cost}")