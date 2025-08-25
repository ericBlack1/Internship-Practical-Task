# Employee Management System

A Django-based employee management system with comprehensive tracking of employees, departments, attendance, and performance, featuring a full REST API built with Django REST Framework, JWT authentication, Swagger documentation, and interactive Chart.js visualizations.

## Features

- **Employee Management**: Store and manage employee information including personal details and department assignments
- **Department Management**: Organize employees into departments
- **Attendance Tracking**: Monitor daily attendance with status tracking (Present/Absent/Late)
- **Performance Reviews**: Track employee performance with 1-5 rating system
- **Admin Interface**: Full-featured Django admin for data management
- **REST API**: Complete CRUD API with filtering, pagination, and search capabilities
- **JWT Authentication**: Secure API endpoints with JSON Web Token authentication
- **Swagger Documentation**: Interactive API documentation with drf-yasg
- **Data Visualization**: Interactive charts using Chart.js for analytics
- **Data Seeding**: Management command to generate realistic test data using Faker

## Models

### Department
- `name`: Department name (unique)
- `created_at`, `updated_at`: Timestamps

### Employee
- `name`: Employee full name
- `email`: Email address (unique, validated)
- `phone_number`: Phone number (validated format)
- `address`: Full address
- `date_of_joining`: Employment start date
- `department`: Foreign key to Department
- `created_at`, `updated_at`: Timestamps
- `years_of_service`: Calculated property

### Attendance
- `employee`: Foreign key to Employee
- `date`: Attendance date
- `status`: Present/Absent/Late
- `created_at`, `updated_at`: Timestamps
- `is_weekend`: Calculated property

### Performance
- `employee`: Foreign key to Employee
- `rating`: 1-5 rating scale
- `review_date`: Performance review date
- `comments`: Optional review comments
- `created_at`, `updated_at`: Timestamps
- `rating_display`: Human-readable rating

## API Features

### REST API Endpoints
- **Departments**: `/api/departments/` - Full CRUD operations
- **Employees**: `/api/employees/` - Full CRUD operations with advanced filtering
- **Attendance**: `/api/attendance/` - Full CRUD operations with statistics
- **Performance**: `/api/performance/` - Full CRUD operations with analytics

### Advanced Features
- **Filtering**: Filter by department, date ranges, ratings, status, etc.
- **Search**: Full-text search across multiple fields
- **Sorting**: Sort by any field in ascending/descending order
- **Pagination**: Configurable page sizes with navigation
- **Statistics**: Built-in analytics and reporting endpoints
- **Custom Actions**: Employee-specific attendance and performance views

### Authentication & Security
- **JWT Authentication**: Secure all endpoints with JSON Web Tokens
- **Public Access**: Employee list accessible without authentication
- **Protected Operations**: All other operations require valid JWT token
- **Token Management**: Access tokens (1 hour) and refresh tokens (1 day)
- **Custom Permissions**: Granular control over endpoint access

### API Documentation
- **Swagger UI**: Interactive API documentation at `/swagger/`
- **ReDoc**: Alternative documentation view at `/redoc/`
- **OpenAPI Schema**: Machine-readable API specification at `/swagger.json`
- **Authentication Support**: Test endpoints with JWT tokens in Swagger

### Data Visualization
- **Charts Dashboard**: Interactive analytics at `/charts/`
- **Department Distribution**: Pie chart showing employees per department
- **Monthly Attendance**: Bar chart showing attendance trends over 6 months
- **Real-time Statistics**: Live dashboard with key metrics
- **Responsive Design**: Mobile-friendly chart interface

## Quick Start Guide

### Prerequisites
- Python 3.8+
- PostgreSQL
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd employee_management
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb -U postgres employee_management

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Configuration
DB_NAME=employee_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Seed Sample Data
```bash
# Generate 40 employees, 8 departments, 90 days of data
python manage.py seed_data

# Or generate custom amount
python manage.py seed_data --employees 50 --departments 10 --days 120
```

### 7. Start Development Server
```bash
python manage.py runserver
```

### 8. Access the System
- **Main Site**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/
- **Swagger Documentation**: http://127.0.0.1:8000/swagger/
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc/
- **Charts Dashboard**: http://127.0.0.1:8000/charts/
- **Browsable API**: http://127.0.0.1:8000/api-auth/

## Authentication

### JWT Authentication Setup
The system uses SimpleJWT for secure authentication:

1. **Login to get tokens**:
   ```bash
   POST /api/auth/login/
   {
       "username": "your_username",
       "password": "your_password"
   }
   ```

2. **Use access token**:
   ```bash
   Authorization: Bearer <your_access_token>
   ```

3. **Refresh expired tokens**:
   ```bash
   POST /api/auth/refresh/
   {
       "refresh_token": "your_refresh_token"
   }
   ```

### Public vs Protected Endpoints
- **Public**: `GET /api/employees/` (employee list)
- **Protected**: All other endpoints require JWT authentication

For detailed authentication information, see [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md).

## API Usage Examples

### Public Access (No Authentication)
```bash
# Get all employees (public endpoint)
curl http://localhost:8000/api/employees/
```

### Authenticated Access
```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token for protected endpoints
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/departments/
```

### Advanced Filtering
```bash
# Filter employees by department
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/employees/?department=1"

# Search employees
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/employees/?search=john"

# Get attendance statistics
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/attendance/statistics/?days=30"
```

### Python Requests Example
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'admin',
    'password': 'admin123'
})
tokens = response.json()

# Use token
headers = {'Authorization': f"Bearer {tokens['access_token']}"}
response = requests.get('http://localhost:8000/api/departments/', headers=headers)
departments = response.json()
```

## Management Commands

### seed_data
Generate realistic test data for development and testing:

```bash
# Basic usage (40 employees, 8 departments, 90 days)
python manage.py seed_data

# Custom amounts
python manage.py seed_data --employees 100 --departments 12 --days 180

# Clear existing data and seed fresh data
python manage.py seed_data --clear

# Help
python manage.py seed_data --help
```

## Data Visualization

### Charts Dashboard
Access interactive analytics at `/charts/`:

- **Employees per Department**: Pie chart showing distribution
- **Monthly Attendance**: Bar chart with 6-month trends
- **Real-time Statistics**: Live dashboard metrics
- **Responsive Design**: Works on all devices

### Chart.js Features
- **Interactive Charts**: Hover effects and tooltips
- **Responsive Design**: Adapts to screen size
- **Real-time Data**: Fetches from API endpoints
- **Professional Styling**: Modern, clean interface

## Testing

### Run API Tests
```bash
python test_api.py
```

### Run JWT Authentication Tests
```bash
python test_jwt_auth.py
```

### Test Management Commands
```bash
python manage.py seed_data --employees 5 --departments 3 --days 7
```

## Project Structure
```
employee_management/
├── employees/
│   ├── models.py          # Department & Employee models
│   ├── serializers.py     # API serializers
│   ├── views.py          # ViewSets with CRUD operations
│   ├── filters.py        # Advanced filtering
│   ├── admin.py          # Admin interface
│   ├── auth.py           # JWT authentication views
│   ├── charts_views.py   # Charts dashboard views
│   ├── permissions.py    # Custom permission classes
│   └── management/       # seed_data command
├── attendance/
│   ├── models.py          # Attendance & Performance models
│   ├── serializers.py     # API serializers
│   ├── views.py          # ViewSets with CRUD operations
│   ├── filters.py        # Advanced filtering
│   ├── admin.py          # Admin interface
│   └── permissions.py    # Permission classes
├── templates/
│   └── charts.html       # Charts dashboard template
├── employee_project/
│   ├── settings.py        # Django settings with DRF & JWT config
│   └── urls.py           # Main URL configuration
├── requirements.txt       # Dependencies
├── README.md             # This file
├── AUTHENTICATION_GUIDE.md # JWT authentication guide
├── API_DOCUMENTATION.md  # Detailed API docs
├── QUICKSTART.md         # Quick start guide
├── test_api.py           # API testing script
└── test_jwt_auth.py      # JWT authentication tests
```

## Database Relationships

- **Department** ← **Employee** (One-to-Many)
- **Employee** ← **Attendance** (One-to-Many)
- **Employee** ← **Performance** (One-to-Many)

## Admin Features

- **Department Admin**: List, search, and filter departments
- **Employee Admin**: Comprehensive employee management with fieldsets
- **Attendance Admin**: Daily attendance tracking with filters
- **Performance Admin**: Performance review management

## API Endpoints

The system provides a complete REST API with:

- **CRUD Operations**: Create, Read, Update, Delete for all models
- **Advanced Filtering**: Filter by any field or combination of fields
- **Search**: Full-text search across multiple fields
- **Sorting**: Sort by any field in any direction
- **Pagination**: Configurable page sizes with navigation
- **Statistics**: Built-in analytics and reporting
- **Custom Actions**: Model-specific operations and views
- **JWT Security**: Secure authentication for all protected endpoints
- **Swagger Docs**: Interactive API documentation and testing
- **Charts API**: Data endpoints for visualizations

## Development Workflow

### 1. Make Changes
- Edit models in `employees/models.py` or `attendance/models.py`
- Update serializers, views, or filters as needed

### 2. Test Changes
```bash
python manage.py makemigrations
python manage.py migrate
python test_api.py
python test_jwt_auth.py
```

### 3. Run Server
```bash
python manage.py runserver
```

### 4. Test in Browser
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- Swagger: http://localhost:8000/swagger/
- Charts: http://localhost:8000/charts/

## Production Deployment

### Security Considerations
1. **Use HTTPS**: Always use HTTPS in production
2. **Secure JWT Keys**: Use strong, unique JWT signing keys
3. **Environment Variables**: Store sensitive data in environment variables
4. **Database Security**: Use strong database passwords and connections
5. **Rate Limiting**: Implement rate limiting for authentication endpoints

### Environment Variables
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=employee_management_prod
DB_USER=prod_user
DB_PASSWORD=strong_password
DB_HOST=your-db-host
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   ```

2. **Migration Errors**
   ```bash
   # Reset migrations if needed
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **JWT Authentication Issues**
   - Check token format (must start with "Bearer ")
   - Verify token expiration
   - Check user permissions in Django admin

4. **Charts Not Loading**
   - Ensure API endpoints are accessible
   - Check browser console for JavaScript errors
   - Verify authentication for protected endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the API documentation at `/swagger/`
3. Check server logs for detailed error messages
4. Use the test scripts to verify functionality

---

**Happy coding! 🚀**

Your Employee Management System is now complete with:
- ✅ Full REST API with JWT authentication
- ✅ Interactive Swagger documentation
- ✅ Beautiful Chart.js visualizations
- ✅ Comprehensive testing suite
- ✅ Production-ready security features
