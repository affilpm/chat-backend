import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRegisterView:
    def setup_method(self):
        self.url = reverse('register')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        self.invalid_payload_password_mismatch = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        }

    def test_register_user_success(self, client):
        response = client.post(self.url, self.valid_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='test@example.com').exists()
        assert response.data['success'] is True
        assert response.data['message'] == "User created successfully"

    def test_register_user_password_mismatch(self, client):
        response = client.post(self.url, self.invalid_payload_password_mismatch)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(email='test2@example.com').exists()

    def test_register_user_duplicate_email(self, client):
        User.objects.create_user(username='existing', email='test@example.com', password='password')
        response = client.post(self.url, self.valid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
