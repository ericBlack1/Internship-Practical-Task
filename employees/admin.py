from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['created_at']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'department', 'date_of_joining', 'years_of_service']
    list_filter = ['department', 'date_of_joining', 'created_at']
    search_fields = ['name', 'email', 'phone_number']
    ordering = ['name']
    date_hierarchy = 'date_of_joining'
    readonly_fields = ['created_at', 'updated_at', 'years_of_service']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_number', 'address')
        }),
        ('Employment Details', {
            'fields': ('department', 'date_of_joining')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
