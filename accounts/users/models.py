from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Define choices for user roles
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    EMPLOYEE = 'employee'
    PATIENT = 'patient'

    ROLE_CHOICES = [
        (SUPERADMIN, 'Superadmin'),
        (ADMIN, 'Admin'),
        (DOCTOR, 'Doctor'),
        (EMPLOYEE, 'Employee'),
        (PATIENT, 'Patient'),
    ]

    # Add a field to represent the user's role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=PATIENT,  # You can set the default role here if needed
    )

    def __str__(self):
        return self.username
