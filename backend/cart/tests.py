from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# доделаю на неделе как нибудь 
# сначала простые тесты

class CartSimpleTestCase(APITestCase):

    def setUp(self):
        """
        Регистрация пользователя, добавление категорий и товаров для провеения тестов
        """
        pass

    def add_item(self):
        """
        Тест добавления товара в корзину
        """
        pass

    def add_and_delete(self):
        """
        Тест добавление и удаление товара из корзины
        """
        pass


