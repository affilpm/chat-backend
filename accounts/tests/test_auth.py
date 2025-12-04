import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestAuthView:
    def setup_method(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.logout_url = reverse('logout')

    def test_login_success(self, client):
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = client.post(self.login_url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access' in response.data['data']
        assert 'refresh' not in response.data['data'] # Refresh token should be in cookie
        assert 'refresh_token' in response.cookies
        assert response.cookies['refresh_token']['httponly'] is True

    def test_login_invalid_credentials(self, client):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = client.post(self.login_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_success(self, client):
        # First login to get the cookie
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        login_response = client.post(self.login_url, data)
        refresh_token = login_response.cookies['refresh_token'].value
        
        # Now refresh using the cookie
        client.cookies['refresh_token'] = refresh_token
        response = client.post(self.refresh_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_logout_success(self, client):
        # First login
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        client.post(self.login_url, data)
        
        # Then logout
        response = client.post(self.logout_url)
        assert response.status_code == status.HTTP_200_OK
        # Check if cookie is deleted (empty string or expired)
        assert response.cookies['refresh_token'].value == ''
