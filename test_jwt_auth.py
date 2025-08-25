#!/usr/bin/env python3
"""
Test script for JWT Authentication and API Security
Run this script to test the authentication system
"""

import os
import sys
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
django.setup()

def test_public_endpoint():
    """Test that the public employees endpoint works without authentication"""
    print("🔓 Testing public endpoint (employees list)...")
    
    try:
        response = requests.get('http://localhost:8000/api/employees/')
        if response.status_code == 200:
            print("   ✅ Public endpoint accessible without authentication")
            data = response.json()
            print(f"   📊 Found {data.get('count', 0)} employees")
            return True
        else:
            print(f"   ❌ Public endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server. Make sure it's running.")
        return False

def test_protected_endpoint():
    """Test that protected endpoints require authentication"""
    print("\n🔒 Testing protected endpoint (departments)...")
    
    try:
        response = requests.get('http://localhost:8000/api/departments/')
        if response.status_code == 401:
            print("   ✅ Protected endpoint correctly requires authentication")
            return True
        else:
            print(f"   ❌ Protected endpoint should require auth but returned: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False

def test_authentication_endpoints():
    """Test JWT authentication endpoints"""
    print("\n🔑 Testing authentication endpoints...")
    
    # Test login endpoint
    try:
        response = requests.post('http://localhost:8000/api/auth/login/', json={
            'username': 'blak',
            'password': '12345678'
        })
        
        if response.status_code == 200:
            print("   ✅ Login endpoint working")
            tokens = response.json()
            print(f"   📝 Got access token: {tokens.get('access_token', '')[:20]}...")
            return tokens
        elif response.status_code == 400:
            print("   ⚠️  Login endpoint working but invalid credentials")
            print("   💡 Create a superuser first: python manage.py createsuperuser")
            return None
        else:
            print(f"   ❌ Login endpoint failed: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return None

def test_authenticated_request(tokens):
    """Test making authenticated requests"""
    if not tokens:
        print("   ⏭️  Skipping authenticated request test (no tokens)")
        return False
    
    print("\n🔐 Testing authenticated request...")
    
    try:
        headers = {
            'Authorization': f"Bearer {tokens['access_token']}"
        }
        
        response = requests.get('http://localhost:8000/api/departments/', headers=headers)
        
        if response.status_code == 200:
            print("   ✅ Authenticated request successful")
            data = response.json()
            print(f"   📊 Found {data.get('count', 0)} departments")
            return True
        else:
            print(f"   ❌ Authenticated request failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False

def test_swagger_documentation():
    """Test Swagger documentation endpoints"""
    print("\n📚 Testing Swagger documentation...")
    
    endpoints = [
        ('/swagger/', 'Swagger UI'),
        ('/redoc/', 'ReDoc'),
        ('/swagger.json', 'Swagger JSON')
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}')
            if response.status_code == 200:
                print(f"   ✅ {name} accessible")
            else:
                print(f"   ❌ {name} failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {name} - Could not connect to server")

def test_token_refresh():
    """Test token refresh functionality"""
    print("\n🔄 Testing token refresh...")
    
    try:
        # First get tokens
        response = requests.post('http://localhost:8000/api/auth/login/', json={
            'username': 'blak',
            'password': '12345678'
        })
        
        if response.status_code == 200:
            tokens = response.json()
            refresh_token = tokens.get('refresh_token')
            
            # Test refresh
            refresh_response = requests.post('http://localhost:8000/api/auth/refresh/', json={
                'refresh_token': refresh_token
            })
            
            if refresh_response.status_code == 200:
                print("   ✅ Token refresh working")
                new_tokens = refresh_response.json()
                print(f"   📝 Got new access token: {new_tokens.get('access_token', '')[:20]}...")
                return True
            else:
                print(f"   ❌ Token refresh failed: {refresh_response.status_code}")
                return False
        else:
            print("   ⏭️  Skipping token refresh test (login failed)")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False

def main():
    """Run all tests"""
    print("🚀 JWT Authentication and API Security Test Suite")
    print("=" * 60)
    
    # Test public endpoint
    public_works = test_public_endpoint()
    
    # Test protected endpoint
    protected_works = test_protected_endpoint()
    
    # Test authentication
    tokens = test_authentication_endpoints()
    
    # Test authenticated requests
    if tokens:
        auth_works = test_authenticated_request(tokens)
    else:
        auth_works = False
    
    # Test token refresh
    refresh_works = test_token_refresh()
    
    # Test Swagger documentation
    test_swagger_documentation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   🔓 Public endpoint: {'✅ PASS' if public_works else '❌ FAIL'}")
    print(f"   🔒 Protected endpoint: {'✅ PASS' if protected_works else '❌ FAIL'}")
    print(f"   🔑 Authentication: {'✅ PASS' if tokens else '❌ FAIL'}")
    print(f"   🔐 Authenticated requests: {'✅ PASS' if auth_works else '❌ FAIL'}")
    print(f"   🔄 Token refresh: {'✅ PASS' if refresh_works else '❌ FAIL'}")
    
    if public_works and protected_works and tokens and auth_works:
        print("\n🎉 All tests passed! JWT authentication is working correctly.")
        print("\n📚 Next steps:")
        print("1. Access Swagger docs: http://localhost:8000/swagger/")
        print("2. Test API endpoints with JWT tokens")
        print("3. Integrate with your frontend application")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the server is running: python manage.py runserver")
        print("2. Create a superuser: python manage.py createsuperuser")
        print("3. Check server logs for errors")

if __name__ == '__main__':
    main()
