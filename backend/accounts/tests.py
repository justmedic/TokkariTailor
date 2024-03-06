from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class TestUserRegistration(APITestCase):
    def test_register_user(self):
        """
        Тестирование успешной регистрации пользователя.
        """
        url = reverse('accounts:user-register')
        data = {
            'username': '',
            'first_name': 'New',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'  
        }
        
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('message' in response.data)
        self.assertEqual(response.data['message'], 'User has been registered successfully')

    def test_register_user_with_invalid_password(self):
        """
        Тестирование регистрации с неверным подтверждением пароля.
        """
        url = reverse('accounts:user-register')
        data = {
            'username': '',
            'first_name': 'Test',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'wrongpassword' 
        }
        
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password2' in response.data)

    def test_register_existing_user(self):
        """
        Тестирование регистрации пользователя, который уже существует.
        """
        User.objects.create_user('existingemail@example.com', 'existingemail@example.com', 'existingpassword')
        url = reverse('accounts:user-register')
        data = {
            'username': 'existingemail@example.com',
            'first_name': 'Existing',
            'email': 'existingemail@example.com',
            'password': 'existingpassword',
            'password2': 'existingpassword'  
        }
        
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('username' in response.data or 'email' in response.data)


class TestUserLoginLogout(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testemail@example.com', password='testpassword123', email = 'testemail@example.com')
        self.login_url = reverse('accounts:user-login')
        self.logout_url = reverse('accounts:user-logout_user')

    def test_user_login(self):
        """
        Тестирование успешного входа пользователя.
        """
        data = {
            'username': 'testemail@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        
    def test_user_login_invalid_credentials(self):
        """
        Тестирование входа с неверными данными пользователя.
        """
        data = {
            'username': 'testemail@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        """
        Тестирование успешного выхода пользователя.
        """
        # Сначала выполним вход
        login_data = {
            'username': 'testemail@example.com',
            'password': 'testpassword123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Теперь выходим
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что токен стал недействительным
        self.assertFalse(Token.objects.filter(key=token).exists())

