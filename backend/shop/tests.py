from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category
import logging



logger = logging.getLogger(__name__) 

class ProductTests(APITestCase):


    def setUp(self):
        category_clothes = Category.objects.create(name="Clothes", slug="clothes",
                                                   characteristics_template={"color": "", "size": ""})
        
        category_electronics = Category.objects.create(name="Electronics", slug="electronics",
                                                       characteristics_template={"warranty": "1 year", "brand": ""})

        Product.objects.create(category=category_clothes, name="T-Shirt", slug="t-shirt", description="A red T-Shirt", 
                               price=29.99, stock=10, available=True, characteristics={"color": "red", "size": "M"})
        Product.objects.create(category=category_clothes, name="Jeans", slug="jeans", description="Blue jeans", 
                               price=59.99, stock=5, available=True, characteristics={"color": "blue", "size": "L"})
        Product.objects.create(category=category_clothes, name="Hat", slug="hat", description="A nice red hat", 
                               price=19.99, stock=15, available=True, characteristics={"color": "red", "size": "S"})

        Product.objects.create(category=category_electronics, name="Smartphone", slug="smartphone", description="Latest model", 
                               price=999.99, stock=30, available=True, characteristics={"warranty": "2 years", "brand": "BrandX"})
        
                               
    def test_filter_products(self):
        """
        Тесты работы динамических фильтров характеристик
        """
        url = reverse('products-filtered')  

        response = self.client.get(url, {'characteristics__color': 'red'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

        response = self.client.get(url, {'characteristics__brand': 'BrandX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

        response = self.client.get(url, {'characteristics__color': 'red', 'characteristics__size': 'M'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  


    def test_filter_products_by_min_price(self):
        """
        Тестирование фильтрации товаров по минимальной цене.
        """
        url = reverse('products-filtered')  

        response = self.client.get(url, {'price__gte': 50})
        # logger.info(f"Фильтра по минимальной цене: {response.data}\n")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)  # Jeans and Smartphone


    def test_filter_products_by_max_price(self):
        """
        Тестирование фильтрации товаров по максимальной цене.
        """
        url = reverse('products-filtered')

        response = self.client.get(url, {'price__lte': 30})
        # logger.info(f"Фильтр по максимальной цене: {response.data}\n")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)  # T-Shirt and Hat


    def test_search_products(self):
        """
        Тестирует работу поиска по продуктам
        """
        url = reverse('products-search')  

        # Тестирование поиска по названию товара
        response = self.client.get(url, {'q': 'T-Shirt'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидаем найти 1 товар с названием "T-Shirt".

        # Тестирование поиска по описанию
        response = self.client.get(url, {'q': 'blue'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ожидается найти 1 товар с описанием, содержащим "blue".

        # Тестирование поиска, который не должен найти результаты
        response = self.client.get(url, {'q': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    

    def create_products(self, num_products=50):
        """ Вспомогательный метод для создания множества товаров. """
        category = Category.objects.create(name="Bulk Category", slug="bulk-category",
                                        characteristics_template={})
        for i in range(num_products):
            Product.objects.create(
                category=category, 
                name=f"Product {i}", slug=f"product-{i}", description=f"Description for product {i}", 
                price=10.00 + i, stock=10 + i, available=True, characteristics={}
            )


    def test_pagination(self):
        """Тестирует пагинацию списка товаров"""
        self.create_products(50)  
        url = reverse('products-list')  

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.assertEqual(len(response.data['results']), 20)
        self.assertTrue(response.data['count'], 50)  
        self.assertIsNotNone(response.data.get('next')) 


        next_page_url = response.data['next']
        response_next_page = self.client.get(next_page_url)
        self.assertEqual(response_next_page.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_next_page.data['results']), 20)  

