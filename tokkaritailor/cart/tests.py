from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cart, CartItem
from shop.models import Product, Category
from django.urls import reverse

class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name="TestCategory", slug="test-category")
        self.product = Product.objects.create(category=self.category, name='Test Product', price=100, stock=10, slug='test-product')
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_cart_creation(self):
        self.assertTrue(isinstance(self.cart, Cart))
        self.assertEqual(self.cart.__str__(), self.cart.user.username)

    def test_cartitem_creation(self):
        self.assertTrue(isinstance(self.cart_item, CartItem))
        self.assertEqual(self.cart.items.count(), 1)


class CartViewsTest(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name="TestCategory", slug="test-category")
        self.product = Product.objects.create(category=self.category, name='Test Product', price=100, stock=10, slug='test-product')
        
    def test_cart_add(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart:cart_detail'))
        self.assertEqual(CartItem.objects.count(), 1)

    def test_cart_remove(self):
        cart_item = CartItem.objects.create(cart=Cart.objects.create(user=self.user), product=self.product)
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart:cart_detail'))
        self.assertEqual(CartItem.objects.count(), 0)
