# JWT Authentication Guide

## Overview

The Employee Management System API now uses JWT (JSON Web Token) authentication to secure all endpoints except for the public employee list endpoint. This guide explains how to authenticate and use the API securely.

## Authentication Endpoints

### 1. Login (Get Access Token)
```bash
POST /api/auth/login/
```

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

### 2. Refresh Token
```bash
POST /api/auth/refresh/
```

**Request Body:**
```json
{
    "refresh_token": "your_refresh_token"
}
```

**Response:**
```json
{
    "access_token": "new_access_token_here"
}
```

### 3. Register (Development Only)
```bash
POST /api/auth/register/
```

**Request Body:**
```json
{
    "username": "newuser",
    "password": "secure_password",
    "email": "user@example.com",
    "first_name": "New",
    "last_name": "User"
}
```

### 4. Built-in JWT Endpoints
```bash
# Get token pair
POST /api/token/

# Refresh token
POST /api/token/refresh/
```

## Using JWT Tokens

### 1. Include Token in Headers
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://localhost:8000/api/employees/1/
```

### 2. Python Requests Example
```python
import requests

# Login to get token
login_data = {
    'username': 'admin',
    'password': 'admin123'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
tokens = response.json()

# Use token for authenticated requests
headers = {
    'Authorization': f"Bearer {tokens['access_token']}"
}

# Get employee details
response = requests.get('http://localhost:8000/api/employees/1/', headers=headers)
employee = response.json()
```

### 3. JavaScript/Fetch Example
```javascript
// Login
const loginResponse = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});

const tokens = await loginResponse.json();

// Use token for authenticated requests
const response = await fetch('/api/employees/1/', {
    headers: {
        'Authorization': `Bearer ${tokens.access_token}`
    }
});

const employee = await response.json();
```

## Public vs Protected Endpoints

### Public Endpoints (No Authentication Required)
- `GET /api/employees/` - List all employees

### Protected Endpoints (Authentication Required)
- `POST /api/employees/` - Create employee
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/{id}/` - Get employee details
- All department endpoints
- All attendance endpoints
- All performance endpoints
- All statistics endpoints

## Token Management

### Token Lifetimes
- **Access Token**: 1 hour
- **Refresh Token**: 1 day

### Best Practices
1. **Store tokens securely**: Use secure storage (not localStorage for production)
2. **Refresh before expiry**: Refresh tokens before they expire
3. **Handle 401 responses**: Implement automatic token refresh on 401 errors
4. **Secure storage**: Use httpOnly cookies or secure storage mechanisms

### Token Refresh Strategy
```python
import requests
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
    
    def login(self, username, password):
        response = requests.post(f'{self.base_url}/api/auth/login/', json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            # Set expiry to 55 minutes (5 minutes before actual expiry)
            self.token_expiry = datetime.now() + timedelta(minutes=55)
            return True
        return False
    
    def refresh_if_needed(self):
        if self.token_expiry and datetime.now() >= self.token_expiry:
            self.refresh_token()
    
    def refresh_token(self):
        response = requests.post(f'{self.base_url}/api/auth/refresh/', json={
            'refresh_token': self.refresh_token
        })
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access_token']
            self.token_expiry = datetime.now() + timedelta(minutes=55)
            return True
        return False
    
    def make_request(self, method, endpoint, **kwargs):
        self.refresh_if_needed()
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        kwargs['headers'] = headers
        
        response = requests.request(method, f'{self.base_url}{endpoint}', **kwargs)
        
        if response.status_code == 401:
            # Try to refresh token once
            if self.refresh_token():
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = requests.request(method, f'{self.base_url}{endpoint}', **kwargs)
        
        return response
```

## Error Handling

### Common HTTP Status Codes
- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: Valid token but insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Authentication Errors
```json
{
    "detail": "Authentication credentials were not provided."
}
```

```json
{
    "detail": "Token is invalid or expired"
}
```

## Security Considerations

### Production Deployment
1. **Use HTTPS**: Always use HTTPS in production
2. **Secure token storage**: Implement secure token storage
3. **Token rotation**: Consider implementing token rotation
4. **Rate limiting**: Implement rate limiting for authentication endpoints
5. **Audit logging**: Log authentication attempts and failures

### Environment Variables
```env
# JWT Settings
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=1:00:00
JWT_REFRESH_TOKEN_LIFETIME=1:00:00:00

# Security Settings
DEBUG=False
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Testing Authentication

### 1. Test Public Endpoint
```bash
# This should work without authentication
curl http://localhost:8000/api/employees/
```

### 2. Test Protected Endpoint
```bash
# This should fail without authentication
curl http://localhost:8000/api/departments/
# Response: {"detail": "Authentication credentials were not provided."}
```

### 3. Test with Valid Token
```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token for protected endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/departments/
```

## Swagger Documentation

Access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

The Swagger documentation includes:
- Authentication requirements for each endpoint
- Request/response schemas
- Interactive testing with JWT tokens
- Example requests and responses

## Troubleshooting

### Common Issues

1. **Token Expired**
   - Use refresh token to get new access token
   - Implement automatic token refresh

2. **Invalid Token Format**
   - Ensure token starts with "Bearer "
   - Check token length and format

3. **CORS Issues**
   - Configure CORS settings for your frontend domain
   - Ensure Authorization header is allowed

4. **Permission Denied**
   - Check user permissions in Django admin
   - Verify token belongs to user with required permissions

### Debug Mode
```python
# In Django settings for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'rest_framework_simplejwt': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Support

For authentication issues:
1. Check Django admin for user permissions
2. Verify token format and expiration
3. Check server logs for detailed error messages
4. Use Swagger documentation for endpoint testing
