from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg
from datetime import date, timedelta
import calendar

from .models import Department, Employee
from attendance.models import Attendance, Performance

def charts_dashboard(request):
    """
    Charts dashboard view with employee and attendance analytics
    Public access allowed for the main dashboard page
    """
    context = {
        'page_title': 'Analytics Dashboard',
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
    }
    
    return render(request, 'charts.html', context)

def api_department_stats(request):
    """
    API endpoint for department statistics (for Chart.js)
    Public access for chart data
    """
    try:
        departments = Department.objects.annotate(
            employee_count=Count('employees')
        ).values('name', 'employee_count').order_by('-employee_count')
        
        return JsonResponse({
            'results': list(departments),
            'total': len(departments)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_attendance_monthly(request):
    """
    API endpoint for monthly attendance statistics (for Chart.js)
    Public access for chart data
    """
    try:
        # Get the last 6 months
        months = []
        present_data = []
        absent_data = []
        late_data = []
        
        current_date = date.today()
        
        for i in range(6):
            # Calculate month start and end
            if current_date.month - i <= 0:
                year = current_date.year - 1
                month = 12 + (current_date.month - i)
            else:
                year = current_date.year
                month = current_date.month - i
            
            month_start = date(year, month, 1)
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year, month + 1, 1) - timedelta(days=1)
            
            # Get attendance data for this month
            month_attendance = Attendance.objects.filter(
                date__range=[month_start, month_end]
            )
            
            total_records = month_attendance.count()
            
            if total_records > 0:
                present_count = month_attendance.filter(status='present').count()
                absent_count = month_attendance.filter(status='absent').count()
                late_count = month_attendance.filter(status='late').count()
                
                # Calculate percentages
                present_pct = round((present_count / total_records) * 100, 1)
                absent_pct = round((absent_count / total_records) * 100, 1)
                late_pct = round((late_count / total_records) * 100, 1)
            else:
                present_pct = absent_pct = late_pct = 0
            
            months.append(month_start.strftime('%b %y'))
            present_data.append(present_pct)
            absent_data.append(absent_pct)
            late_data.append(late_pct)
        
        # Reverse to show oldest to newest
        months.reverse()
        present_data.reverse()
        absent_data.reverse()
        late_data.reverse()
        
        return JsonResponse({
            'months': months,
            'present': present_data,
            'absent': absent_data,
            'late': late_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_dashboard_stats(request):
    """
    API endpoint for dashboard statistics
    Public access for chart data
    """
    try:
        # Employee statistics
        total_employees = Employee.objects.count()
        total_departments = Department.objects.count()
        
        # Attendance statistics (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        attendance_records = Attendance.objects.filter(date__gte=thirty_days_ago)
        
        total_attendance = attendance_records.count()
        if total_attendance > 0:
            present_count = attendance_records.filter(status='present').count()
            attendance_rate = round((present_count / total_attendance) * 100, 1)
        else:
            attendance_rate = 0
        
        # Performance statistics
        performance_records = Performance.objects.all()
        if performance_records.exists():
            avg_performance = round(
                performance_records.aggregate(avg_rating=Avg('rating'))['avg_rating'], 1
            )
        else:
            avg_performance = 0
        
        return JsonResponse({
            'total_employees': total_employees,
            'total_departments': total_departments,
            'attendance_rate': attendance_rate,
            'avg_performance': avg_performance
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
