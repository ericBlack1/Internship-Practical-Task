from django.shortcuts import render
from django.db.models import Count, Avg, Q
from datetime import date

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Department, Employee
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, EmployeeDetailSerializer
)
from .filters import DepartmentFilter, EmployeeFilter
from .permissions import EmployeeListPermission, DepartmentPermission

class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model with CRUD operations"""
    queryset = Department.objects.annotate(
        employee_count=Count('employees')
    ).all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DepartmentFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'employee_count']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return DepartmentSerializer
        return DepartmentSerializer
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a specific department"""
        department = self.get_object()
        employees = department.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get department statistics"""
        departments = Department.objects.annotate(
            employee_count=Count('employees')
        ).values('name', 'employee_count')
        
        total_employees = sum(dept['employee_count'] for dept in departments)
        avg_employees = total_employees / len(departments) if departments else 0
        
        return Response({
            'total_departments': len(departments),
            'total_employees': total_employees,
            'average_employees_per_department': round(avg_employees, 2),
            'departments': list(departments)
        })

class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for Employee model with CRUD operations"""
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeListPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['name', 'email', 'phone_number']
    ordering_fields = [
        'name', 'email', 'date_of_joining', 'created_at', 
        'department__name', 'years_of_service'
    ]
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a specific employee"""
        employee = self.get_object()
        from attendance.models import Attendance
        attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
        
        from attendance.serializers import AttendanceSerializer
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance records for a specific employee"""
        employee = self.get_object()
        from attendance.models import Performance
        performance_records = Performance.objects.filter(employee=employee).order_by('-review_date')
        
        from attendance.serializers import PerformanceSerializer
        serializer = PerformanceSerializer(performance_records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get employee statistics"""
        total_employees = Employee.objects.count()
        departments = Department.objects.annotate(
            employee_count=Count('employees')
        ).values('name', 'employee_count')
        
        # Calculate average years of service
        employees_with_service = Employee.objects.all()
        total_years = sum(emp.years_of_service for emp in employees_with_service)
        avg_years = total_years / total_employees if total_employees > 0 else 0
        
        return Response({
            'total_employees': total_employees,
            'average_years_of_service': round(avg_years, 2),
            'departments': list(departments),
            'recent_hires': Employee.objects.order_by('-date_of_joining')[:5].values(
                'name', 'department__name', 'date_of_joining'
            )
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search across multiple fields"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Query parameter "q" is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employees = Employee.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(department__name__icontains=query)
        ).select_related('department')
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
