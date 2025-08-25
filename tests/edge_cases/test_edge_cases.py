import pytest
from django.urls import reverse
from employees.models import Department, Employee
from datetime import date

pytestmark = pytest.mark.django_db

def test_missing_jwt_requires_auth(api_client):
    # departments list requires auth
    resp = api_client.get(reverse('department-list'))
    assert resp.status_code == 401


def test_nonexistent_id_returns_404(auth_client):
    resp = auth_client.get(reverse('employee-detail', args=[999999]))
    assert resp.status_code == 404


def test_delete_already_deleted_record(auth_client):
    dept = Department.objects.create(name='Temp')
    url = reverse('department-detail', args=[dept.id])
    # First delete
    resp = auth_client.delete(url)
    assert resp.status_code == 204
    # Second delete should 404
    resp = auth_client.delete(url)
    assert resp.status_code == 404


def test_health_endpoint(api_client):
    resp = api_client.get('/health')
    assert resp.status_code == 200
    assert resp.json().get('status') == 'ok'
