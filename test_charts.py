#!/usr/bin/env python3
"""
Test script for Charts Dashboard and Visualization API
Run this script to test the charts functionality
"""

import os
import sys
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')
django.setup()

def test_charts_endpoints():
    """Test the charts API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Charts Dashboard and API Endpoints...")
    print("=" * 60)
    
    # Test 1: Charts dashboard page
    print("\n📊 Testing Charts Dashboard Page...")
    try:
        response = requests.get(f"{base_url}/charts/")
        if response.status_code == 200:
            print("   ✅ Charts dashboard page accessible")
            if "Analytics Dashboard" in response.text:
                print("   ✅ Dashboard content loaded correctly")
            else:
                print("   ⚠️  Dashboard content may not be loading properly")
        else:
            print(f"   ❌ Charts dashboard failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server. Make sure it's running.")
        return False
    
    # Test 2: Department stats API
    print("\n📈 Testing Department Stats API...")
    try:
        response = requests.get(f"{base_url}/api/charts/department-stats/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Department stats API working")
            print(f"   📝 Found {data.get('total', 0)} departments")
            if data.get('results'):
                print(f"   📊 Sample data: {data['results'][0] if data['results'] else 'No data'}")
        else:
            print(f"   ❌ Department stats API failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False
    
    # Test 3: Monthly attendance API
    print("\n📅 Testing Monthly Attendance API...")
    try:
        response = requests.get(f"{base_url}/api/charts/attendance-monthly/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Monthly attendance API working")
            print(f"   📝 Found {len(data.get('months', []))} months of data")
            if data.get('months'):
                print(f"   📊 Sample months: {data['months'][:3]}")
        else:
            print(f"   ❌ Monthly attendance API failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False
    
    # Test 4: Dashboard stats API
    print("\n📊 Testing Dashboard Stats API...")
    try:
        response = requests.get(f"{base_url}/api/charts/dashboard-stats/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Dashboard stats API working")
            print(f"   📝 Total employees: {data.get('total_employees', 0)}")
            print(f"   📝 Total departments: {data.get('total_departments', 0)}")
            print(f"   📝 Attendance rate: {data.get('attendance_rate', 0)}%")
            print(f"   📝 Avg performance: {data.get('avg_performance', 0)}")
        else:
            print(f"   ❌ Dashboard stats API failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to server.")
        return False
    
    return True

def test_charts_template():
    """Test the charts template file"""
    print("\n📄 Testing Charts Template...")
    
    template_path = "templates/charts.html"
    if os.path.exists(template_path):
        print("   ✅ Charts template file exists")
        
        with open(template_path, 'r') as f:
            content = f.read()
            
        # Check for required elements
        required_elements = [
            'Chart.js',
            'departmentChart',
            'attendanceChart',
            'Analytics Dashboard',
            'Employees per Department',
            'Monthly Attendance Overview'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if not missing_elements:
            print("   ✅ All required chart elements present")
        else:
            print(f"   ⚠️  Missing elements: {missing_elements}")
            
    else:
        print("   ❌ Charts template file not found")
        return False
    
    return True

def test_charts_views():
    """Test the charts views module"""
    print("\n🔍 Testing Charts Views Module...")
    
    try:
        from employees import charts_views
        
        # Check if required functions exist
        required_functions = [
            'charts_dashboard',
            'api_department_stats',
            'api_attendance_monthly',
            'api_dashboard_stats'
        ]
        
        missing_functions = []
        for func_name in required_functions:
            if not hasattr(charts_views, func_name):
                missing_functions.append(func_name)
        
        if not missing_functions:
            print("   ✅ All required chart view functions present")
        else:
            print(f"   ❌ Missing functions: {missing_functions}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Could not import charts_views: {e}")
        return False
    
    return True

def main():
    """Run all charts tests"""
    print("🚀 Charts Dashboard and Visualization Test Suite")
    print("=" * 60)
    
    # Test charts template
    template_ok = test_charts_template()
    
    # Test charts views
    views_ok = test_charts_views()
    
    # Test charts endpoints
    endpoints_ok = test_charts_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Charts Test Results Summary:")
    print(f"   📄 Template: {'✅ PASS' if template_ok else '❌ FAIL'}")
    print(f"   🔍 Views: {'✅ PASS' if views_ok else '❌ FAIL'}")
    print(f"   🌐 Endpoints: {'✅ PASS' if endpoints_ok else '❌ FAIL'}")
    
    if template_ok and views_ok and endpoints_ok:
        print("\n🎉 All charts tests passed! Your visualization system is working correctly.")
        print("\n📚 Next steps:")
        print("1. Access charts dashboard: http://localhost:8000/charts/")
        print("2. View interactive charts and analytics")
        print("3. Customize chart colors and styling as needed")
        print("4. Add more chart types for additional insights")
    else:
        print("\n⚠️  Some charts tests failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the server is running: python manage.py runserver")
        print("2. Check that templates directory is properly configured")
        print("3. Verify charts_views.py is properly imported")
        print("4. Check server logs for any errors")

if __name__ == '__main__':
    main()
