from django.test import TestCase
from employees.models import Department, Employee
from datetime import date
from faker import Faker

class SeededCRUDTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        Faker.seed(12345)
        cls.dept = Department.objects.create(name='Engineering')

    def test_create_employee_happy_path(self):
        emp = Employee.objects.create(
            name='Alice Smith',
            email='alice.smith@example.com',
            phone_number='+12345678901',
            address='123 Main St',
            date_of_joining=date(2023, 1, 1),
            department=self.dept
        )
        self.assertEqual(emp.department.name, 'Engineering')
        self.assertTrue(Employee.objects.filter(email='alice.smith@example.com').exists())

    def test_create_employee_duplicate_email_error(self):
        Employee.objects.create(
            name='Bob',
            email='dup@example.com',
            phone_number='+12345678902',
            address='Addr',
            date_of_joining=date(2023, 1, 1),
            department=self.dept
        )
        with self.assertRaises(Exception):
            Employee.objects.create(
                name='Charlie',
                email='dup@example.com',
                phone_number='+12345678903',
                address='Addr2',
                date_of_joining=date(2023, 2, 1),
                department=self.dept
            )

    def test_department_update_and_delete(self):
        dept = Department.objects.create(name='HR')
        dept.name = 'Human Resources'
        dept.save()
        self.assertEqual(Department.objects.get(id=dept.id).name, 'Human Resources')
        dept.delete()
        self.assertFalse(Department.objects.filter(id=dept.id).exists())
