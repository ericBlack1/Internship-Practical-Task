#!/usr/bin/env python3
"""
Test script for the Employee Management System API
Run this script to test the API endpoints
"""

import os
import sys
import django
import requests
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
django.setup()

def test_api_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8000/api"
    
    print("🧪 Testing Employee Management System API...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/departments/")
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print(f"❌ API server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure the server is running.")
        print("   Run: python manage.py runserver")
        return False
    
    # Test 2: Test departments endpoint
    print("\n📋 Testing Departments endpoint...")
    try:
        response = requests.get(f"{base_url}/departments/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('count', 0)} departments")
            if data.get('results'):
                print(f"   📝 First department: {data['results'][0]['name']}")
        else:
            print(f"   ❌ Departments endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing departments: {e}")
    
    # Test 3: Test employees endpoint
    print("\n👥 Testing Employees endpoint...")
    try:
        response = requests.get(f"{base_url}/employees/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('count', 0)} employees")
            if data.get('results'):
                print(f"   📝 First employee: {data['results'][0]['name']}")
        else:
            print(f"   ❌ Employees endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing employees: {e}")
    
    # Test 4: Test attendance endpoint
    print("\n📅 Testing Attendance endpoint...")
    try:
        response = requests.get(f"{base_url}/attendance/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('count', 0)} attendance records")
        else:
            print(f"   ❌ Attendance endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing attendance: {e}")
    
    # Test 5: Test performance endpoint
    print("\n⭐ Testing Performance endpoint...")
    try:
        response = requests.get(f"{base_url}/performance/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('count', 0)} performance records")
        else:
            print(f"   ❌ Performance endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing performance: {e}")
    
    # Test 6: Test statistics endpoints
    print("\n📊 Testing Statistics endpoints...")
    try:
        # Department statistics
        response = requests.get(f"{base_url}/departments/statistics/")
        if response.status_code == 200:
            print("   ✅ Department statistics working")
        
        # Employee statistics
        response = requests.get(f"{base_url}/employees/statistics/")
        if response.status_code == 200:
            print("   ✅ Employee statistics working")
        
        # Attendance statistics
        response = requests.get(f"{base_url}/attendance/statistics/")
        if response.status_code == 200:
            print("   ✅ Attendance statistics working")
        
        # Performance statistics
        response = requests.get(f"{base_url}/performance/statistics/")
        if response.status_code == 200:
            print("   ✅ Performance statistics working")
            
    except Exception as e:
        print(f"   ❌ Error testing statistics: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\n📚 Next steps:")
    print("1. Access the API at: http://localhost:8000/api/")
    print("2. View API documentation at: http://localhost:8000/docs/")
    print("3. Use the browsable API at: http://localhost:8000/api-auth/")
    print("4. Admin interface at: http://localhost:8000/admin/")
    
    return True

def test_management_command():
    """Test the seed_data management command"""
    print("\n🌱 Testing seed_data management command...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capture output
        out = StringIO()
        
        # Test with minimal data
        call_command('seed_data', '--employees', '5', '--departments', '3', '--days', '7', stdout=out)
        
        output = out.getvalue()
        if "Database seeding completed successfully" in output:
            print("   ✅ seed_data command working correctly")
            print("   📊 Generated sample data for testing")
        else:
            print("   ❌ seed_data command failed")
            print(f"   Output: {output}")
            
    except Exception as e:
        print(f"   ❌ Error testing seed_data command: {e}")

if __name__ == '__main__':
    print("🚀 Employee Management System API Test Suite")
    print("=" * 50)
    
    # Test management command first
    test_management_command()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n✨ All tests completed!")
