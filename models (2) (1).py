from django.db import models

# Create your models here.
from django.db import models

class Employee(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Chef', 'Chef'),
        ('Server', 'Server'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def calculate_payroll(self):
        return self.salary * self.hours_worked

    def __str__(self):
        return f"{self.name} ({self.role})"
