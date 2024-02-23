from django.test import TestCase
from shop.models import Category, Product, ProductImage
from shop.api.serializers import ProductSerializer, CategorySerializer, CategoryDetailSerializer, ProductImageSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

class ProductSerializerTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые данные для категории
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        # Создаем тестовый продукт
        self.product = Product.objects.create(category=self.category, name="Laptop", slug="laptop", description="A powerful laptop", price=1000, stock=4, available=True)

    def test_product_serialization(self):
        # Тестируем сериализацию продукта
        product = Product.objects.get(name="Laptop")
        serializer = ProductSerializer(product)
        expected_data = {
            'category': self.category.id,
            'name': 'Laptop',
            'slug': 'laptop',
            'description': 'A powerful laptop',
            'price': '1000.00',
            'stock': 4,
            'available': True,
            'images': []
        }
        self.assertEqual(serializer.data, expected_data)

class CategorySerializerTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые данные для проверки сериализатора категорий
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.subcategory = Category.objects.create(name="Laptops", slug="laptops", parent=self.category)

    def test_category_serialization(self):
        # Тестируем сериализацию категории
        category = Category.objects.get(name="Electronics")
        serializer = CategorySerializer(category)
        expected_data = {
            'id': self.category.id,
            'name': 'Electronics',
            'slug': 'electronics',
            'parent': None,
            'url': reverse('category-detail', args=[self.category.id])
        }
        self.assertEqual(serializer.data, expected_data)

    def test_category_detail_serialization(self):
        # Тестируем сериализацию подробной информации о категории
        category = Category.objects.get(name="Electronics")
        serializer = CategoryDetailSerializer(category)
        expected_data = {
            'id': self.category.id,
            'name': 'Electronics',
            'slug': 'electronics',
            'parent': None,
            'children': [
                {
                    'id': self.subcategory.id,
                    'name': 'Laptops',
                    'slug': 'laptops',
                    'parent': self.category.id,
                    'url': reverse('category-detail', args=[self.subcategory.id])
                }
            ],
            'products': []
        }
        self.assertCountEqual(serializer.data['children'], expected_data['children'])
