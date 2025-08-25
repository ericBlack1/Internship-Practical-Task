from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Attendance, Performance
from .serializers import (
    AttendanceSerializer, AttendanceDetailSerializer,
    PerformanceSerializer, PerformanceDetailSerializer
)
from .filters import AttendanceFilter, PerformanceFilter
from .permissions import AttendancePermission, PerformancePermission

# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Attendance model with CRUD operations"""
    queryset = Attendance.objects.select_related('employee', 'employee__department').all()
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AttendanceFilter
    search_fields = ['employee__name', 'employee__email', 'employee__department__name']
    ordering_fields = [
        'date', 'status', 'created_at', 'employee__name', 
        'employee__department__name'
    ]
    ordering = ['-date', 'employee__name']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return AttendanceDetailSerializer
        return AttendanceSerializer
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's attendance records"""
        from datetime import date
        today = date.today()
        today_attendance = self.queryset.filter(date=today)
        serializer = AttendanceSerializer(today_attendance, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get attendance statistics"""
        from datetime import date, timedelta
        
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Filter attendance records for the date range
        attendance_records = self.queryset.filter(
            date__range=[start_date, end_date]
        )
        
        # Calculate statistics
        total_records = attendance_records.count()
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        late_count = attendance_records.filter(status='late').count()
        
        # Calculate attendance rate
        attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
        
        # Department-wise statistics
        dept_stats = attendance_records.values('employee__department__name').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='present')),
            absent=Count('id', filter=Q(status='absent')),
            late=Count('id', filter=Q(status='late'))
        )
        
        return Response({
            'period': f'{days} days',
            'start_date': start_date,
            'end_date': end_date,
            'total_records': total_records,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'attendance_rate': round(attendance_rate, 2),
            'department_statistics': list(dept_stats)
        })
    
    @action(detail=False, methods=['get'])
    def employee_summary(self, request):
        """Get attendance summary for a specific employee"""
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response(
                {'error': 'employee_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from employees.models import Employee
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get attendance records for the employee
        employee_attendance = self.queryset.filter(employee=employee)
        
        # Calculate summary
        total_days = employee_attendance.count()
        present_days = employee_attendance.filter(status='present').count()
        absent_days = employee_attendance.filter(status='absent').count()
        late_days = employee_attendance.filter(status='late').count()
        
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        
        return Response({
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department.name
            },
            'attendance_summary': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'late_days': late_days,
                'attendance_rate': round(attendance_rate, 2)
            }
        })

class PerformanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Performance model with CRUD operations"""
    queryset = Performance.objects.select_related('employee', 'employee__department').all()
    serializer_class = PerformanceSerializer
    permission_classes = [PerformancePermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PerformanceFilter
    search_fields = [
        'employee__name', 'employee__email', 'employee__department__name', 'comments'
    ]
    ordering_fields = [
        'rating', 'review_date', 'created_at', 'employee__name',
        'employee__department__name'
    ]
    ordering = ['-review_date', 'employee__name']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return PerformanceDetailSerializer
        return PerformanceSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get performance statistics"""
        # Overall statistics
        total_reviews = self.queryset.count()
        avg_rating = self.queryset.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # Rating distribution
        rating_distribution = self.queryset.values('rating').annotate(
            count=Count('id')
        ).order_by('rating')
        
        # Department-wise average ratings
        dept_ratings = self.queryset.values('employee__department__name').annotate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        ).order_by('-avg_rating')
        
        # Top performers (rating 4-5)
        top_performers = self.queryset.filter(rating__gte=4).select_related('employee')[:10]
        top_performers_data = PerformanceSerializer(top_performers, many=True).data
        
        return Response({
            'overall_statistics': {
                'total_reviews': total_reviews,
                'average_rating': round(avg_rating, 2)
            },
            'rating_distribution': list(rating_distribution),
            'department_ratings': list(dept_ratings),
            'top_performers': top_performers_data
        })
    
    @action(detail=False, methods=['get'])
    def employee_performance(self, request):
        """Get performance history for a specific employee"""
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response(
                {'error': 'employee_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from employees.models import Employee
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get performance records for the employee
        employee_performance = self.queryset.filter(employee=employee).order_by('-review_date')
        
        # Calculate summary
        total_reviews = employee_performance.count()
        avg_rating = employee_performance.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        latest_review = employee_performance.first()
        
        # Rating trend
        rating_trend = employee_performance.values('review_date', 'rating').order_by('review_date')
        
        return Response({
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department.name
            },
            'performance_summary': {
                'total_reviews': total_reviews,
                'average_rating': round(avg_rating, 2),
                'latest_review': PerformanceSerializer(latest_review).data if latest_review else None
            },
            'rating_trend': list(rating_trend),
            'all_reviews': PerformanceSerializer(employee_performance, many=True).data
        })
