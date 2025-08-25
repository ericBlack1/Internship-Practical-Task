from django.contrib import admin
from .models import Attendance, Performance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'is_weekend', 'created_at']
    list_filter = ['status', 'date', 'created_at', 'employee__department']
    search_fields = ['employee__name', 'employee__email']
    ordering = ['-date', 'employee__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'is_weekend']
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('employee', 'date', 'status')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'rating', 'rating_display', 'review_date', 'created_at']
    list_filter = ['rating', 'review_date', 'created_at', 'employee__department']
    search_fields = ['employee__name', 'employee__email', 'comments']
    ordering = ['-review_date', 'employee__name']
    date_hierarchy = 'review_date'
    readonly_fields = ['created_at', 'updated_at', 'rating_display']
    
    fieldsets = (
        ('Performance Information', {
            'fields': ('employee', 'rating', 'review_date', 'comments')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
