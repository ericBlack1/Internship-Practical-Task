from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import auth
from . import charts_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet)
router.register(r'employees', views.EmployeeViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/login/', auth.login_view, name='auth_login'),
    path('auth/refresh/', auth.refresh_token_view, name='auth_refresh'),
    path('auth/register/', auth.register_view, name='auth_register'),
    # Charts and analytics endpoints
    path('charts/dashboard/', charts_views.charts_dashboard, name='charts_dashboard'),
    path('charts/department-stats/', charts_views.api_department_stats, name='api_department_stats'),
    path('charts/attendance-monthly/', charts_views.api_attendance_monthly, name='api_attendance_monthly'),
    path('charts/dashboard-stats/', charts_views.api_dashboard_stats, name='api_dashboard_stats'),
]
