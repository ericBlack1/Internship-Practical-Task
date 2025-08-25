#!/usr/bin/env python3
"""
Sample data script for Employee Management System
Run this script to populate the database with sample data
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
django.setup()

from employees.models import Department, Employee
from attendance.models import Attendance, Performance

def create_sample_data():
    """Create sample departments, employees, attendance, and performance records"""
    
    print("Creating sample data...")
    
    # Create Departments
    departments = [
        Department.objects.get_or_create(name="Engineering")[0],
        Department.objects.get_or_create(name="Marketing")[0],
        Department.objects.get_or_create(name="Human Resources")[0],
        Department.objects.get_or_create(name="Finance")[0],
        Department.objects.get_or_create(name="Sales")[0],
    ]
    
    print(f"Created {len(departments)} departments")
    
    # Create Employees
    employees_data = [
        {
            'name': 'John Smith',
            'email': 'john.smith@company.com',
            'phone_number': '+1234567890',
            'address': '123 Main St, City, State 12345',
            'date_of_joining': date(2020, 1, 15),
            'department': departments[0],  # Engineering
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@company.com',
            'phone_number': '+1234567891',
            'address': '456 Oak Ave, City, State 12345',
            'date_of_joining': date(2019, 6, 20),
            'department': departments[1],  # Marketing
        },
        {
            'name': 'Michael Brown',
            'email': 'michael.brown@company.com',
            'phone_number': '+1234567892',
            'address': '789 Pine Rd, City, State 12345',
            'date_of_joining': date(2021, 3, 10),
            'department': departments[2],  # HR
        },
        {
            'name': 'Emily Davis',
            'email': 'emily.davis@company.com',
            'phone_number': '+1234567893',
            'address': '321 Elm St, City, State 12345',
            'date_of_joining': date(2018, 11, 5),
            'department': departments[3],  # Finance
        },
        {
            'name': 'David Wilson',
            'email': 'david.wilson@company.com',
            'phone_number': '+1234567894',
            'address': '654 Maple Dr, City, State 12345',
            'date_of_joining': date(2022, 2, 28),
            'department': departments[4],  # Sales
        },
    ]
    
    employees = []
    for emp_data in employees_data:
        employee, created = Employee.objects.get_or_create(
            email=emp_data['email'],
            defaults=emp_data
        )
        employees.append(employee)
        if created:
            print(f"Created employee: {employee.name}")
    
    print(f"Created {len(employees)} employees")
    
    # Create Attendance records for the last 30 days
    attendance_records = []
    today = date.today()
    
    for i in range(30):
        current_date = today - timedelta(days=i)
        
        for employee in employees:
            # Skip weekends for some employees
            if current_date.weekday() >= 5 and employee.name in ['John Smith', 'Sarah Johnson']:
                continue
                
            # Random attendance status (for demo purposes)
            import random
            status_choices = ['present', 'present', 'present', 'late', 'absent']
            status = random.choice(status_choices)
            
            # Create attendance record
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=current_date,
                defaults={'status': status}
            )
            attendance_records.append(attendance)
    
    print(f"Created {len(attendance_records)} attendance records")
    
    # Create Performance records
    performance_records = []
    
    for employee in employees:
        # Create performance review for each employee
        review_date = date.today() - timedelta(days=random.randint(1, 90))
        rating = random.randint(3, 5)  # Most employees perform well
        
        performance, created = Performance.objects.get_or_create(
            employee=employee,
            review_date=review_date,
            defaults={
                'rating': rating,
                'comments': f"Annual performance review for {employee.name}. Overall performance: {rating}/5."
            }
        )
        performance_records.append(performance)
        
        if created:
            print(f"Created performance review for {employee.name}: {rating}/5")
    
    print(f"Created {len(performance_records)} performance records")
    
    print("\nSample data creation completed!")
    print(f"Total records created:")
    print(f"- Departments: {Department.objects.count()}")
    print(f"- Employees: {Employee.objects.count()}")
    print(f"- Attendance: {Attendance.objects.count()}")
    print(f"- Performance: {Performance.objects.count()}")

def show_sample_queries():
    """Demonstrate some useful queries with the models"""
    
    print("\n" + "="*50)
    print("SAMPLE QUERIES AND USAGE EXAMPLES")
    print("="*50)
    
    # Get all employees in Engineering department
    engineering_employees = Employee.objects.filter(department__name='Engineering')
    print(f"\nEngineering employees: {[emp.name for emp in engineering_employees]}")
    
    # Get employees with more than 2 years of service
    experienced_employees = [emp for emp in Employee.objects.all() if emp.years_of_service > 2]
    print(f"\nEmployees with >2 years service: {[emp.name for emp in experienced_employees]}")
    
    # Get today's attendance
    today_attendance = Attendance.objects.filter(date=date.today())
    print(f"\nToday's attendance: {[(att.employee.name, att.status) for att in today_attendance]}")
    
    # Get high performers (rating 4-5)
    high_performers = Performance.objects.filter(rating__gte=4)
    print(f"\nHigh performers: {[(perf.employee.name, perf.rating) for perf in high_performers]}")
    
    # Get department statistics
    print(f"\nDepartment statistics:")
    for dept in Department.objects.all():
        emp_count = dept.employees.count()
        print(f"- {dept.name}: {emp_count} employees")

if __name__ == '__main__':
    try:
        create_sample_data()
        show_sample_queries()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the database is set up and migrations are applied.")
        sys.exit(1)
