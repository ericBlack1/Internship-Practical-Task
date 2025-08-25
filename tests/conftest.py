import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker

@pytest.fixture(scope='session')
def faker_seeded():
    fake = Faker()
    Faker.seed(12345)
    return fake

@pytest.fixture
def user_db(db):
    user = User.objects.create_user(username='tester', password='password123', email='t@e.com')
    return user

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, user_db):
    refresh = RefreshToken.for_user(user_db)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return api_client
