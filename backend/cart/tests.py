from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import CustomUser
from shop.models import Product, Category
from cart.models import Cart, CartItem

from shop.api.serializers import ProductSerializer

class CartTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testemail@example.com',
            username='testemail@example.com',
            password='testpassword123'
        )
        self.login_url = reverse('accounts:user-login')
        self.logout_url = reverse('accounts:user-logout_user')
        self.client = APIClient()
        self.client.login(email='testemail@example.com', password='testpassword123')
        

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

        factory = APIRequestFactory() # я хз че это опять блять сраный кастыль в этом джанго как же он бесит
        request = factory.get('/')

        product_info = ProductSerializer(self.product, context={'request': request}).data
        print("Информация о продукте, добавленном в корзину:")
        print(product_info)

    def test_add_multiple_items_to_cart(self):

        product2 = Product.objects.create(
            category=self.category, name="Smartphone", slug="smartphone",
            price=500, stock=10, available=True, characteristics={})
        

        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        CartItem.objects.create(cart=self.cart, product=product2, quantity=2)
        

        self.assertEqual(self.cart.items.count(), 2)
        self.assertEqual(CartItem.objects.filter(cart=self.cart, product=product2).count(), 1)
        self.assertEqual(CartItem.objects.get(cart=self.cart, product=product2).quantity, 2)

