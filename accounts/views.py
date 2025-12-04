from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from common.mixins.api import BaseAPIMixin

from .serializers import RegisterSerializer
from .services import create_user

class RegisterView(BaseAPIMixin, APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=RegisterSerializer, responses=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        return self.created(message="User created successfully")