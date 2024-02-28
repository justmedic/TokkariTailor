from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserRegistrationSerializer

    @action(detail=False, methods=['post'], url_path= 'register' , url_name= 'register')
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User has been registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
