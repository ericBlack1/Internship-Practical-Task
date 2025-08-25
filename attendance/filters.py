import django_filters
from django.db.models import Q
from .models import Attendance, Performance
from employees.models import Department

class AttendanceFilter(django_filters.FilterSet):
    """Filter for Attendance model"""
    employee_name = django_filters.CharFilter(field_name='employee__name', lookup_expr='icontains')
    employee_email = django_filters.CharFilter(field_name='employee__email', lookup_expr='icontains')
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    department_name = django_filters.CharFilter(field_name='employee__department__name', lookup_expr='icontains')
    
    # Date filters
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    date_range = django_filters.DateFromToRangeFilter(field_name='date')
    
    # Status filters
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)
    
    # Search across multiple fields
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Attendance
        fields = {
            'employee': ['exact'],
            'date': ['exact', 'gte', 'lte'],
            'status': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }
    
    def search_filter(self, queryset, name, value):
        """Search across employee name, email, and department"""
        return queryset.filter(
            Q(employee__name__icontains=value) |
            Q(employee__email__icontains=value) |
            Q(employee__department__name__icontains=value)
        )

class PerformanceFilter(django_filters.FilterSet):
    """Filter for Performance model"""
    employee_name = django_filters.CharFilter(field_name='employee__name', lookup_expr='icontains')
    employee_email = django_filters.CharFilter(field_name='employee__email', lookup_expr='icontains')
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    department_name = django_filters.CharFilter(field_name='employee__department__name', lookup_expr='icontains')
    
    # Rating filters
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    rating_range = django_filters.RangeFilter(field_name='rating')
    
    # Review date filters
    review_date_after = django_filters.DateFilter(field_name='review_date', lookup_expr='gte')
    review_date_before = django_filters.DateFilter(field_name='review_date', lookup_expr='lte')
    review_date_range = django_filters.DateFromToRangeFilter(field_name='review_date')
    
    # Search across multiple fields
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Performance
        fields = {
            'employee': ['exact'],
            'rating': ['exact', 'gte', 'lte'],
            'review_date': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'gte', 'lte'],
        }
    
    def search_filter(self, queryset, name, value):
        """Search across employee name, email, department, and comments"""
        return queryset.filter(
            Q(employee__name__icontains=value) |
            Q(employee__email__icontains=value) |
            Q(employee__department__name__icontains=value) |
            Q(comments__icontains=value)
        )
