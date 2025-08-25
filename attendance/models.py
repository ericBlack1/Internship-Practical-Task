from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from employees.models import Employee

class Attendance(models.Model):
    """Attendance model for tracking employee attendance"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'employee__name']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['employee', 'date']  # One record per employee per day

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.get_status_display()}"

    @property
    def is_weekend(self):
        """Check if the attendance date falls on a weekend"""
        return self.date.weekday() >= 5

class Performance(models.Model):
    """Performance model for tracking employee performance ratings"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='performance_records'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1"),
            MaxValueValidator(5, message="Rating cannot exceed 5")
        ]
    )
    review_date = models.DateField()
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_date', 'employee__name']
        verbose_name = 'Performance'
        verbose_name_plural = 'Performance Records'

    def __str__(self):
        return f"{self.employee.name} - {self.review_date} - Rating: {self.rating}/5"

    @property
    def rating_display(self):
        """Get a human-readable rating display"""
        rating_texts = {
            1: 'Poor',
            2: 'Below Average',
            3: 'Average',
            4: 'Good',
            5: 'Excellent'
        }
        return rating_texts.get(self.rating, 'Unknown')
