from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from common.mixins.api import BaseAPIMixin

from .serializers import RegisterSerializer, LoginSerializer
from .services import create_user, login_user
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

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

class LoginView(BaseAPIMixin, APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=LoginSerializer, responses=None)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tokens = login_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if tokens is None:
            return Response(
                {"detail": "Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        response = self.success(
            data={'access': tokens['access']}, 
            message="Login successful"
        )
        
        response.set_cookie(
            'refresh_token',
            tokens['refresh'],
            httponly=True,
            samesite='Lax',
            secure=False, # Set to True in production
            max_age=7 * 24 * 60 * 60 # 7 days
        )
        
        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        return response

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        data = request.data
        if refresh_token:
            if hasattr(data, 'copy'):
                data = data.copy()
            else:
                data = dict(data)
            data['refresh'] = refresh_token
            
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        if response.status_code == 200 and 'refresh' in response.data:
             # If rotation is enabled, simplejwt might return a new refresh token
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                samesite='Lax',
                secure=False, # Set to True in production
                max_age=7 * 24 * 60 * 60 # 7 days
            )
            del response.data['refresh']
            
        return response


