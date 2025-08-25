from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import date, timedelta
import random

from employees.models import Department, Employee
from attendance.models import Attendance, Performance

class Command(BaseCommand):
    help = 'Seed the database with fake employee data using Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employees',
            type=int,
            default=40,
            help='Number of employees to create (default: 40)'
        )
        parser.add_argument(
            '--departments',
            type=int,
            default=8,
            help='Number of departments to create (default: 8)'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days of attendance data to generate (default: 90)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(42)  # For reproducible results
        
        num_employees = options['employees']
        num_departments = options['departments']
        num_days = options['days']
        clear_existing = options['clear']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting to seed database with {num_employees} employees, '
                f'{num_departments} departments, and {num_days} days of data...'
            )
        )
        
        if clear_existing:
            self.stdout.write('Clearing existing data...')
            Performance.objects.all().delete()
            Attendance.objects.all().delete()
            Employee.objects.all().delete()
            Department.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))
        
        # Create departments
        self.stdout.write('Creating departments...')
        departments = []
        department_names = [
            'Engineering', 'Marketing', 'Human Resources', 'Finance', 'Sales',
            'Operations', 'Research & Development', 'Customer Support',
            'Legal', 'Information Technology', 'Product Management', 'Quality Assurance'
        ]
        
        for i in range(min(num_departments, len(department_names))):
            dept, created = Department.objects.get_or_create(
                name=department_names[i]
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'  Created department: {dept.name}')
        
        # Create employees
        self.stdout.write(f'Creating {num_employees} employees...')
        employees = []
        
        for i in range(num_employees):
            # Generate realistic employee data
            first_name = fake.first_name()
            last_name = fake.last_name()
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
            
            # Generate phone number that fits within 15 character limit
            phone = f"+1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"
            
            address = fake.address()
            
            # Random joining date within last 5 years
            years_ago = random.randint(0, 5)
            months_ago = random.randint(0, 12)
            days_ago = random.randint(0, 30)
            date_of_joining = date.today() - timedelta(
                days=years_ago * 365 + months_ago * 30 + days_ago
            )
            
            # Random department assignment
            department = random.choice(departments)
            
            employee = Employee.objects.create(
                name=name,
                email=email,
                phone_number=phone,
                address=address,
                date_of_joining=date_of_joining,
                department=department
            )
            employees.append(employee)
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'  Created {i + 1} employees...')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(employees)} employees'))
        
        # Create attendance records
        self.stdout.write(f'Creating attendance records for {num_days} days...')
        attendance_count = 0
        today = date.today()
        
        for i in range(num_days):
            current_date = today - timedelta(days=i)
            
            for employee in employees:
                # Skip weekends for some employees (realistic work pattern)
                if current_date.weekday() >= 5 and random.random() < 0.7:
                    continue
                
                # Generate realistic attendance patterns
                if random.random() < 0.85:  # 85% present
                    status = 'present'
                elif random.random() < 0.7:  # 70% of remaining are late
                    status = 'late'
                else:
                    status = 'absent'
                
                # Create attendance record
                attendance, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=current_date,
                    defaults={'status': status}
                )
                
                if created:
                    attendance_count += 1
                
                # Progress update every 1000 records
                if attendance_count % 1000 == 0 and attendance_count > 0:
                    self.stdout.write(f'  Created {attendance_count} attendance records...')
        
        self.stdout.write(self.style.SUCCESS(f'Created {attendance_count} attendance records'))
        
        # Create performance records
        self.stdout.write('Creating performance records...')
        performance_count = 0
        
        for employee in employees:
            # Create 1-3 performance reviews per employee
            num_reviews = random.randint(1, 3)
            
            for review_num in range(num_reviews):
                # Review date within last 2 years
                months_ago = random.randint(1, 24)
                days_ago = random.randint(0, 30)
                review_date = date.today() - timedelta(
                    days=months_ago * 30 + days_ago
                )
                
                # Realistic rating distribution (bell curve)
                rating_weights = [0.05, 0.15, 0.30, 0.35, 0.15]  # 1-5 ratings
                rating = random.choices(range(1, 6), weights=rating_weights)[0]
                
                # Generate realistic comments
                if rating >= 4:
                    comments = f"Excellent performance by {employee.name}. Shows strong initiative and delivers high-quality work consistently."
                elif rating == 3:
                    comments = f"Good performance by {employee.name}. Meets expectations and shows potential for growth."
                else:
                    comments = f"Performance review for {employee.name}. Areas for improvement identified and development plan created."
                
                performance, created = Performance.objects.get_or_create(
                    employee=employee,
                    review_date=review_date,
                    defaults={
                        'rating': rating,
                        'comments': comments
                    }
                )
                
                if created:
                    performance_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {performance_count} performance records'))
        
        # Final summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Database seeding completed successfully!\n'
                f'📊 Summary:\n'
                f'  • Departments: {Department.objects.count()}\n'
                f'  • Employees: {Employee.objects.count()}\n'
                f'  • Attendance Records: {Attendance.objects.count()}\n'
                f'  • Performance Records: {Performance.objects.count()}\n'
                f'\nYou can now run the development server and test the API endpoints!'
            )
        )
