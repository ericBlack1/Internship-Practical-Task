import pytest
from django.urls import reverse
from employees.models import Department, Employee
from attendance.models import Attendance, Performance
from datetime import date

pytestmark = pytest.mark.django_db

def create_employee(name, email, department):
    return Employee.objects.create(
        name=name,
        email=email,
        phone_number='+12345678901',
        address='Addr',
        date_of_joining=date(2022, 1, 1),
        department=department,
    )

def test_employee_list_public(api_client):
    url = reverse('employee-list')  # router default name pattern
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert 'results' in resp.json()

def test_employee_crud_auth(auth_client):
    dept = Department.objects.create(name='Sales')
    # Create
    url = reverse('employee-list')
    payload = {
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'phone_number': '+12345678909',
        'address': '123 Main',
        'date_of_joining': '2023-01-01',
        'department': dept.id,
    }
    resp = auth_client.post(url, payload, format='json')
    assert resp.status_code == 201
    emp_id = resp.json()['id']

    # Retrieve
    resp = auth_client.get(reverse('employee-detail', args=[emp_id]))
    assert resp.status_code == 200

    # Update
    resp = auth_client.patch(reverse('employee-detail', args=[emp_id]), {'address': '456 Oak'}, format='json')
    assert resp.status_code == 200
    assert resp.json()['address'] == '456 Oak'

    # Delete
    resp = auth_client.delete(reverse('employee-detail', args=[emp_id]))
    assert resp.status_code == 204


def test_department_crud_and_filtering(auth_client):
    Department.objects.bulk_create([Department(name='Eng'), Department(name='HR')])
    url = reverse('department-list')
    # list
    resp = auth_client.get(url)
    assert resp.status_code == 200
    # filter by name icontains
    resp = auth_client.get(url + '?name=eng')
    assert resp.status_code == 200


def test_attendance_performance_crud(auth_client):
    dept = Department.objects.create(name='Ops')
    emp = create_employee('Ann', 'ann@example.com', dept)

    # Attendance create unique (employee, date)
    url = reverse('attendance-list')
    payload = {'employee': emp.id, 'date': '2024-01-10', 'status': 'present'}
    resp = auth_client.post(url, payload, format='json')
    assert resp.status_code == 201
    # Duplicate same day should 400 via serializer unique_together check route will raise
    resp = auth_client.post(url, payload, format='json')
    assert resp.status_code in (400, 409)

    # Performance create
    url = reverse('performance-list')
    perf_payload = {'employee': emp.id, 'rating': 4, 'review_date': '2024-02-01', 'comments': 'Good'}
    resp = auth_client.post(url, perf_payload, format='json')
    assert resp.status_code == 201


def test_pagination_sorting(auth_client):
    dept = Department.objects.create(name='QA')
    for i in range(25):
        create_employee(f'User {i:02d}', f'user{i}@example.com', dept)
    url = reverse('employee-list')
    # page 1 default 20
    resp = auth_client.get(url)
    data = resp.json()
    assert data['count'] >= 25
    assert len(data['results']) == 20
    # page 2
    resp = auth_client.get(url + '?page=2')
    assert resp.status_code == 200
    # ordering
    resp = auth_client.get(url + '?ordering=-date_of_joining')
    assert resp.status_code == 200
