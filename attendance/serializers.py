from rest_framework import serializers
from .models import Attendance, Performance
from employees.serializers import EmployeeSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    is_weekend = serializers.ReadOnlyField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'department_name',
            'date', 'status', 'is_weekend', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_weekend']
    
    def validate(self, data):
        """Custom validation for attendance records"""
        # Check if attendance record already exists for this employee on this date
        if Attendance.objects.filter(
            employee=data['employee'], 
            date=data['date']
        ).exists():
            raise serializers.ValidationError(
                "An attendance record already exists for this employee on this date."
            )
        
        # Validate that the date is not in the future
        from datetime import date
        if data['date'] > date.today():
            raise serializers.ValidationError("Attendance date cannot be in the future.")
        
        return data

class AttendanceDetailSerializer(AttendanceSerializer):
    """Detailed serializer for Attendance with nested employee data"""
    employee = EmployeeSerializer(read_only=True)
    
    class Meta(AttendanceSerializer.Meta):
        fields = AttendanceSerializer.Meta.fields + ['employee']

class PerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Performance model"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    rating_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Performance
        fields = [
            'id', 'employee', 'employee_name', 'department_name',
            'rating', 'rating_display', 'review_date', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'rating_display']
    
    def validate_rating(self, value):
        """Custom validation for rating"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate_review_date(self, value):
        """Custom validation for review date"""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Review date cannot be in the future.")
        return value

class PerformanceDetailSerializer(PerformanceSerializer):
    """Detailed serializer for Performance with nested employee data"""
    employee = EmployeeSerializer(read_only=True)
    
    class Meta(PerformanceSerializer.Meta):
        fields = PerformanceSerializer.Meta.fields + ['employee']
