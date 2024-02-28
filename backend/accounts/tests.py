from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class TestUserRegistration(APITestCase):
    def test_register_user(self):
        """
        Тестирование успешной регистрации пользователя.
        """
        url = reverse('accounts:user-register')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'  # Подтверждение пароля, если вы это реализовали в сериализаторе
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)
        self.assertEqual(response.data['message'], 'User has been registered successfully')

    def test_register_user_with_invalid_password(self):
        """
        Тестирование регистрации с неверным подтверждением пароля.
        """
        url = reverse('accounts:user-register')
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'wrongpassword'  # Неверное подтверждение пароля
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)

    def test_register_existing_user(self):
        """
        Тестирование регистрации пользователя, который уже существует.
        """
        User.objects.create_user('existinguser', 'existingemail@example.com', 'existingpassword')
        url = reverse('accounts:user-register')
        data = {
            'username': 'existinguser',
            'first_name': 'Existing',
            'email': 'existingemail@example.com',
            'password': 'existingpassword',
            'password2': 'existingpassword'  # Такой же пароль
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('username' in response.data or 'email' in response.data)
