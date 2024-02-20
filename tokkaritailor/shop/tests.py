from django.test import TestCase
from .models import Category, Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class CategoryModelTest(TestCase):
    """Тестирование иерархии категорий."""
    def setUp(self):
        self.main_category = Category.objects.create(name='Одежда', slug='odezhda')
        self.sub_category = Category.objects.create(name='Зимняя одежда', slug='zimnyaya-odezhda', parent=self.main_category)
        self.sub_sub_category = Category.objects.create(name='Штаны', slug='shtany', parent=self.sub_category)

    def test_category_creation(self):
        self.assertTrue(isinstance(self.main_category, Category))
        self.assertTrue(isinstance(self.sub_category, Category))
        self.assertTrue(isinstance(self.sub_sub_category, Category))
        self.assertEqual(self.main_category.__str__(), 'Одежда')
        self.assertEqual(self.sub_category.__str__(), 'Зимняя одежда')
        self.assertEqual(self.sub_sub_category.__str__(), 'Штаны')
    
    def test_category_relationships(self):
        self.assertIsNone(self.main_category.parent)
        self.assertEqual(self.sub_category.parent, self.main_category)
        self.assertEqual(self.sub_sub_category.parent, self.sub_category)

class ProductModelTest(TestCase):
    """Тестирование создания и атрибутов продуктов."""
    def setUp(self):
        self.category = Category.objects.create(name='Книги', slug='knigi')
        self.product = Product.objects.create(
            category=self.category,
            name='Приключения Шерлока Холмса',
            slug='priklyucheniya-sherloka-holmsa',
            description='Книга о приключениях известного детектива',
            price=500.00,
            stock=10,
            available=True
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), 'Приключения Шерлока Холмса')
        self.assertEqual(self.product.category, self.category)

class CategoryProductTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(category=self.category, name='Laptop', slug='laptop', description='A powerful laptop.', price=1000.00, stock=50, available=True)

    def test_create_category(self):
        """
        тест новые категории создание
        """
        url = reverse('category-list')  
        data = {'name': 'Books', 'slug': 'books'}
        response = self.client.post(url, data, format='json', enforce_csrf_checks=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=2).name, 'Books')

    def test_create_product(self):
        """
        тест создание новых продуктов
        """
        url = reverse('product-list')  
        data = {
            'category_id': self.category.id,
            'name': 'Smartphone',
            'slug': 'smartphone',
            'description': 'A latest smartphone.',
            'price': 500.00,
            'stock': 30,
            'available': True
        }
        response = self.client.post(url, data, format='json', enforce_csrf_checks=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=2).name, 'Smartphone')

    def test_list_categories(self):
        """
        тест список категорий
        """
        url = reverse('category-list') 
        response = self.client.get(url, format='json', enforce_csrf_checks=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['name'], 'Electronics')

    def test_list_products(self):
        """
        тест списка продуктов
        """
        url = reverse('product-list')  
        response = self.client.get(url, format='json', enforce_csrf_checks=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['name'], 'Laptop')