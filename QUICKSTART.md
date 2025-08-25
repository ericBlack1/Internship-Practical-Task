# Quick Start Guide

Get up and running with the Employee Management System API in minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Database
```bash
# Create PostgreSQL database
createdb -U postgres employee_management

# Run migrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Seed Sample Data
```bash
# Generate 40 employees, 8 departments, 90 days of data
python manage.py seed_data
```

### 5. Start Server
```bash
python manage.py runserver
```

## 🎯 API Quick Test

### Test Basic Endpoints
```bash
# Get all departments
curl http://localhost:8000/api/departments/

# Get all employees
curl http://localhost:8000/api/employees/

# Get attendance records
curl http://localhost:8000/api/attendance/

# Get performance records
curl http://localhost:8000/api/performance/
```

### Test Filtering
```bash
# Filter employees by department
curl "http://localhost:8000/api/employees/?department=1"

# Search employees
curl "http://localhost:8000/api/employees/?search=john"

# Filter attendance by status
curl "http://localhost:8000/api/attendance/?status=present"
```

### Test Statistics
```bash
# Get department statistics
curl http://localhost:8000/api/departments/statistics/

# Get attendance statistics
curl "http://localhost:8000/api/attendance/statistics/?days=30"

# Get performance statistics
curl http://localhost:8000/api/performance/statistics/
```

## 🔧 Development Workflow

### 1. Make Model Changes
```python
# Edit models in employees/models.py or attendance/models.py
```

### 2. Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Test API
```bash
python test_api.py
```

### 4. Run Server
```bash
python manage.py runserver
```

## 📚 Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/departments/` | GET, POST | List/Create departments |
| `/api/departments/{id}/` | GET, PUT, PATCH, DELETE | Department CRUD |
| `/api/employees/` | GET, POST | List/Create employees |
| `/api/employees/{id}/` | GET, PUT, PATCH, DELETE | Employee CRUD |
| `/api/attendance/` | GET, POST | List/Create attendance |
| `/api/attendance/{id}/` | GET, PUT, PATCH, DELETE | Attendance CRUD |
| `/api/performance/` | GET, POST | List/Create performance |
| `/api/performance/{id}/` | GET, PUT, PATCH, DELETE | Performance CRUD |

## 🔍 Advanced Features

### Filtering Examples
```bash
# Date range filtering
curl "http://localhost:8000/api/employees/?date_joined_after=2020-01-01&date_joined_before=2023-12-31"

# Rating filtering
curl "http://localhost:8000/api/performance/?min_rating=4&max_rating=5"

# Multiple filters
curl "http://localhost:8000/api/attendance/?status=present&date_after=2024-01-01"
```

### Sorting Examples
```bash
# Sort by name
curl "http://localhost:8000/api/employees/?ordering=name"

# Sort by date (newest first)
curl "http://localhost:8000/api/attendance/?ordering=-date"

# Sort by rating (highest first)
curl "http://localhost:8000/api/performance/?ordering=-rating"
```

### Pagination
```bash
# Change page size
curl "http://localhost:8000/api/employees/?page_size=50"

# Navigate pages
curl "http://localhost:8000/api/employees/?page=2"
```

## 🧪 Testing

### Run Test Suite
```bash
python test_api.py
```

### Test Management Commands
```bash
# Test with minimal data
python manage.py seed_data --employees 5 --departments 3 --days 7

# Test data clearing
python manage.py seed_data --clear
```

## 🌐 Web Interface

- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/docs/
- **Browsable API**: http://localhost:8000/api-auth/

## 📖 Next Steps

1. **Explore the API**: Use the browsable API to test endpoints
2. **Read Documentation**: Check `API_DOCUMENTATION.md` for detailed API specs
3. **Customize Models**: Modify models to fit your specific needs
4. **Add Authentication**: Implement JWT or OAuth for production
5. **Add Tests**: Write comprehensive test coverage
6. **Deploy**: Set up production environment

## 🆘 Common Issues

### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql
```

### Migration Errors
```bash
# Reset migrations if needed
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

### Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 🎉 You're Ready!

Your Employee Management System API is now running! Start building your frontend application or integrate with existing systems.

Happy coding! 🚀
