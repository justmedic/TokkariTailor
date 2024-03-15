from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category
import logging
import timeit
from faker import Faker
import random
from statistics import mean, stdev



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

    def test_filter_products_by_min_price_performance(self):
        """
        Стресс-тестирование фильтрации товаров по минимальной цене
        с измерением времени отклика.
        """
        def do_request():
            self.client.get(reverse('products-filtered'), {'price__gte': 50})
        
        number_of_requests = 1000
        

        total_time = timeit.timeit(do_request, number=number_of_requests)
        
        average_time = total_time / number_of_requests
        logger.info(f"Среднее время отклика при {number_of_requests} запросах: {average_time} секунд.")
        
        self.assertLess(average_time, 0.1, "Среднее время отклика превышает предельно допустимое значение.")


class ProductStressTests(APITestCase):

    def setUp(self):
        faker = Faker()  
        

        category_clothes = Category.objects.create(name="Clothes", slug="clothes",
                                                   characteristics_template={"color": "", "size": ""})
        
        category_electronics = Category.objects.create(name="Electronics", slug="electronics",
                                                       characteristics_template={"warranty": "1 year", "brand": ""})
        
        categories = [category_clothes, category_electronics]
        characteristics_clothes = ["red", "blue", "green", "black"], ["S", "M", "L", "XL"]
        characteristics_electronics = ["1 year", "2 years", "3 years"], ["BrandX", "BrandY", "BrandZ"]
        
        print('Запись тестовых товаров в бд')
        for _ in range(1000):
            category = random.choice(categories)
            
            if category == category_clothes:
                color, size = random.choices(characteristics_clothes[0]), random.choice(characteristics_clothes[1])
                characteristics = {"color": color, "size": size}
            else:
                warranty, brand = random.choice(characteristics_electronics[0]), random.choice(characteristics_electronics[1])
                characteristics = {"warranty": warranty, "brand": brand}
            
            Product.objects.create(
                category=category,
                name=faker.word(),  # Генерируем случайное название товара
                slug=faker.slug(),  # Генерируем случайный slug
                description=faker.text(),  # Генерируем случайное описание
                price=faker.random_number(digits=4),  # Генерируем случайную цену
                stock=faker.random_number(digits=3),  # Случайное количество на складе
                available=faker.boolean(),  # Случайная доступность
                characteristics=characteristics
            )
        print('запись окончена')

    def test_filter_products_staff_performance(self):
        """Проведение стресс-теста на фильтрацию товаров."""

        def do_request_and_measure_time():
            start_time = timeit.default_timer()
            self.client.get(reverse('products-filtered'), {'price__gte': 50})
            end_time = timeit.default_timer()
            return end_time - start_time
        
        number_of_requests = 10  # изменить для выбора нагрузки на сервер

        times = []
        print('Начаты тестовые реквесты')
        for _ in range(number_of_requests):
            elapsed_time = do_request_and_measure_time()
            times.append(elapsed_time)

        avg_time = mean(times)
        std_dev_time = stdev(times) if len(times) > 1 else 0


        logger.info(f"Выполнено {number_of_requests} запросов.")
        logger.info(f"Среднее время отклика: {avg_time:.4f} сек.")
        logger.info(f"Стандартное отклонение времени отклика: {std_dev_time:.4f} сек.")

    
        expected_max_avg_time = 0.5  
        expected_max_std_dev = 0.1  


        self.assertLess(avg_time, expected_max_avg_time, "Среднее время отклика выше ожидаемого.")
        self.assertLess(std_dev_time, expected_max_std_dev, "Дисперсия времени отклика выше ожидаемой.")