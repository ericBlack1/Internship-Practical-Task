from rest_framework import permissions

class AttendancePermission(permissions.BasePermission):
    """
    Permission class for attendance operations
    """
    
    def has_permission(self, request, view):
        # Require authentication for all attendance operations
        return request.user and request.user.is_authenticated

class PerformancePermission(permissions.BasePermission):
    """
    Permission class for performance operations
    """
    
    def has_permission(self, request, view):
        # Require authentication for all performance operations
        return request.user and request.user.is_authenticated
