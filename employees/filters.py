import django_filters
from django.db.models import Q
from .models import Employee, Department

class DepartmentFilter(django_filters.FilterSet):
    """Filter for Department model"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Department
        fields = {
            'name': ['exact', 'icontains', 'startswith'],
            'created_at': ['exact', 'gte', 'lte'],
        }

class EmployeeFilter(django_filters.FilterSet):
    """Filter for Employee model"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    department_name = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains')
    
    # Date range filters
    date_joined_after = django_filters.DateFilter(field_name='date_of_joining', lookup_expr='gte')
    date_joined_before = django_filters.DateFilter(field_name='date_of_joining', lookup_expr='lte')
    
    # Years of service filters
    min_years_service = django_filters.NumberFilter(method='filter_min_years_service')
    max_years_service = django_filters.NumberFilter(method='filter_max_years_service')
    
    # Search across multiple fields
    search = django_filters.CharFilter(method='search_filter')
    
    class Meta:
        model = Employee
        fields = {
            'name': ['exact', 'icontains', 'startswith'],
            'email': ['exact', 'icontains'],
            'phone_number': ['exact', 'icontains'],
            'department': ['exact'],
            'date_of_joining': ['exact', 'gte', 'lte'],
        }
    
    def filter_min_years_service(self, queryset, name, value):
        """Filter employees with minimum years of service"""
        from datetime import date
        today = date.today()
        min_date = today.replace(year=today.year - int(value))
        return queryset.filter(date_of_joining__lte=min_date)
    
    def filter_max_years_service(self, queryset, name, value):
        """Filter employees with maximum years of service"""
        from datetime import date
        today = date.today()
        max_date = today.replace(year=today.year - int(value))
        return queryset.filter(date_of_joining__gte=max_date)
    
    def search_filter(self, queryset, name, value):
        """Search across name, email, and phone number"""
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone_number__icontains=value)
        )
