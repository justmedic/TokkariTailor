from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category
import logging



logger = logging.getLogger(__name__) 

class ProductTests(APITestCase):
    """
    Тестирует работу динамических фильтров 
    """

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
        Тесты работы динамических фильтров
        """
        url = reverse('products-filtered')  

        response = self.client.get(url, {'characteristics__color': 'red'})
        # logger.info(f"Response data: {response.data}") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

        response = self.client.get(url, {'characteristics__brand': 'BrandX'})
        # logger.info(f"Response data: {response.data}")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

        response = self.client.get(url, {'characteristics__color': 'red', 'characteristics__size': 'M'})
        # logger.info(f"Response data: {response.data}") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

