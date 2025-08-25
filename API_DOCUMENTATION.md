# Employee Management System API Documentation

## Overview

The Employee Management System provides a comprehensive REST API for managing employees, departments, attendance, and performance records. The API is built using Django REST Framework with full CRUD operations, filtering, pagination, and search capabilities.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API requires authentication. You can authenticate using:
- Session authentication (for web browsers)
- Basic authentication (for API clients)

## Endpoints

### 1. Departments

#### List Departments
```
GET /api/departments/
```

**Query Parameters:**
- `search`: Search departments by name
- `ordering`: Sort by `name`, `created_at`, `employee_count`
- `page`: Page number for pagination

**Example Response:**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Engineering",
            "employee_count": 12,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

#### Get Department Details
```
GET /api/departments/{id}/
```

#### Create Department
```
POST /api/departments/
```

**Request Body:**
```json
{
    "name": "New Department"
}
```

#### Update Department
```
PUT /api/departments/{id}/
PATCH /api/departments/{id}/
```

#### Delete Department
```
DELETE /api/departments/{id}/
```

#### Get Department Employees
```
GET /api/departments/{id}/employees/
```

#### Get Department Statistics
```
GET /api/departments/statistics/
```

### 2. Employees

#### List Employees
```
GET /api/employees/
```

**Query Parameters:**
- `search`: Search across name, email, phone number
- `department`: Filter by department ID
- `department_name`: Filter by department name
- `date_joined_after`: Filter by minimum join date
- `date_joined_before`: Filter by maximum join date
- `min_years_service`: Filter by minimum years of service
- `max_years_service`: Filter by maximum years of service
- `ordering`: Sort by various fields
- `page`: Page number for pagination

**Example Response:**
```json
{
    "count": 40,
    "next": "http://localhost:8000/api/employees/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "John Smith",
            "email": "john.smith@company.com",
            "phone_number": "+1234567890",
            "address": "123 Main St, City, State 12345",
            "date_of_joining": "2020-01-15",
            "department": 1,
            "department_name": "Engineering",
            "years_of_service": 4,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

#### Get Employee Details
```
GET /api/employees/{id}/
```

#### Create Employee
```
POST /api/employees/
```

**Request Body:**
```json
{
    "name": "Jane Doe",
    "email": "jane.doe@company.com",
    "phone_number": "+1234567891",
    "address": "456 Oak Ave, City, State 12345",
    "date_of_joining": "2023-06-01",
    "department": 2
}
```

#### Update Employee
```
PUT /api/employees/{id}/
PATCH /api/employees/{id}/
```

#### Delete Employee
```
DELETE /api/employees/{id}/
```

#### Get Employee Attendance
```
GET /api/employees/{id}/attendance/
```

#### Get Employee Performance
```
GET /api/employees/{id}/performance/
```

#### Get Employee Statistics
```
GET /api/employees/statistics/
```

#### Search Employees
```
GET /api/employees/search/?q=john
```

### 3. Attendance

#### List Attendance Records
```
GET /api/attendance/
```

**Query Parameters:**
- `search`: Search across employee name, email, department
- `employee`: Filter by employee ID
- `employee_name`: Filter by employee name
- `department`: Filter by department ID
- `status`: Filter by status (present/absent/late)
- `date_after`: Filter by minimum date
- `date_before`: Filter by maximum date
- `date_range`: Filter by date range
- `ordering`: Sort by various fields
- `page`: Page number for pagination

**Example Response:**
```json
{
    "count": 1200,
    "next": "http://localhost:8000/api/attendance/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "employee": 1,
            "employee_name": "John Smith",
            "department_name": "Engineering",
            "date": "2024-01-15",
            "status": "present",
            "is_weekend": false,
            "created_at": "2024-01-15T09:00:00Z",
            "updated_at": "2024-01-15T09:00:00Z"
        }
    ]
}
```

#### Get Today's Attendance
```
GET /api/attendance/today/
```

#### Get Attendance Statistics
```
GET /api/attendance/statistics/?days=30
```

#### Get Employee Attendance Summary
```
GET /api/attendance/employee_summary/?employee_id=1
```

### 4. Performance

#### List Performance Records
```
GET /api/performance/
```

**Query Parameters:**
- `search`: Search across employee name, email, department, comments
- `employee`: Filter by employee ID
- `rating`: Filter by rating (1-5)
- `min_rating`: Filter by minimum rating
- `max_rating`: Filter by maximum rating
- `rating_range`: Filter by rating range
- `review_date_after`: Filter by minimum review date
- `review_date_before`: Filter by maximum review date
- `ordering`: Sort by various fields
- `page`: Page number for pagination

**Example Response:**
```json
{
    "count": 80,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "employee": 1,
            "employee_name": "John Smith",
            "department_name": "Engineering",
            "rating": 4,
            "rating_display": "Good",
            "review_date": "2024-01-01",
            "comments": "Excellent performance by John Smith. Shows strong initiative.",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

#### Get Performance Statistics
```
GET /api/performance/statistics/
```

#### Get Employee Performance History
```
GET /api/performance/employee_performance/?employee_id=1
```

## Filtering Examples

### Filter Employees by Department
```
GET /api/employees/?department=1
```

### Filter Employees by Date Range
```
GET /api/employees/?date_joined_after=2020-01-01&date_joined_before=2023-12-31
```

### Filter Attendance by Status and Date
```
GET /api/attendance/?status=present&date_after=2024-01-01
```

### Filter Performance by Rating Range
```
GET /api/performance/?min_rating=4&max_rating=5
```

## Search Examples

### Search Employees
```
GET /api/employees/?search=john
```

### Search Attendance Records
```
GET /api/attendance/?search=engineering
```

### Search Performance Records
```
GET /api/performance/?search=excellent
```

## Sorting Examples

### Sort Employees by Name
```
GET /api/employees/?ordering=name
```

### Sort Employees by Years of Service (Descending)
```
GET /api/employees/?ordering=-years_of_service
```

### Sort Attendance by Date (Newest First)
```
GET /api/attendance/?ordering=-date
```

## Pagination

All list endpoints support pagination with a default page size of 20. The response includes:
- `count`: Total number of items
- `next`: URL for the next page
- `previous`: URL for the previous page
- `results`: Array of items for the current page

### Change Page Size
```
GET /api/employees/?page_size=50
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Example Error Response:**
```json
{
    "error": "Employee not found"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## Testing the API

### Using curl

```bash
# Get all employees
curl -X GET "http://localhost:8000/api/employees/" \
  -H "Authorization: Basic base64_encoded_credentials"

# Create a new employee
curl -X POST "http://localhost:8000/api/employees/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic base64_encoded_credentials" \
  -d '{
    "name": "New Employee",
    "email": "new.employee@company.com",
    "phone_number": "+1234567890",
    "address": "123 New St, City, State 12345",
    "date_of_joining": "2024-01-01",
    "department": 1
  }'
```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000/api"

# Authentication
auth = ('username', 'password')

# Get all departments
response = requests.get(f"{base_url}/departments/", auth=auth)
departments = response.json()

# Create a new department
new_dept = {
    "name": "New Department"
}
response = requests.post(f"{base_url}/departments/", json=new_dept, auth=auth)
```

## Management Commands

### Seed Database with Sample Data

```bash
# Generate 40 employees, 8 departments, 90 days of data
python manage.py seed_data

# Generate custom amount of data
python manage.py seed_data --employees 50 --departments 10 --days 120

# Clear existing data and seed fresh data
python manage.py seed_data --clear
```

## Development

### Running the Development Server

```bash
python manage.py runserver
```

### Accessing the API

- API Root: http://localhost:8000/api/
- Admin Interface: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/docs/
- Browsable API: http://localhost:8000/api-auth/

### Making Changes

1. Update models in `employees/models.py` or `attendance/models.py`
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update serializers if needed
4. Test the API endpoints
5. Update this documentation
