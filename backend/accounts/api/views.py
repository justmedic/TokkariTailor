from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser


class UserViewSet(viewsets.GenericViewSet):
    """
    ViewSet для пользователей, поддерживает регистрацию, вход и выход.
    """
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от типа действия,
        исполненного во ViewSet.
        """
        if self.action == 'register':
            return UserRegistrationSerializer
        
        elif self.action == 'login':
            return UserLoginSerializer
        
        
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], url_path='register', url_name='register')
    def register(self, request, *args, **kwargs):
        """
        Регистрирует нового пользователя.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User has been registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login', url_name='login')
    def login(self, request, *args, **kwargs):
        """
        Авторизует пользователя и возвращает токен.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout_user', url_name='logout_user')
    def logout_user(self, request):
        
        """
        Выход пользователя из системы.
        Удаляет токен авторизации пользователя.
        """
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except (AttributeError, ObjectDoesNotExist):
                pass
            
        logout(request)  # Вызывает Django logout для удаления данных сессии.
        return Response({"message": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)
