from rest_framework import permissions

class EmployeeListPermission(permissions.BasePermission):
    """
    Custom permission to allow public access to employee list
    but require authentication for other operations
    """
    
    def has_permission(self, request, view):
        # Allow public access to GET requests for employee list
        if view.action == 'list' and request.method == 'GET':
            return True
        
        # Require authentication for all other operations
        return request.user and request.user.is_authenticated

class DepartmentPermission(permissions.BasePermission):
    """
    Permission class for department operations
    """
    
    def has_permission(self, request, view):
        # Require authentication for all department operations
        return request.user and request.user.is_authenticated

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
