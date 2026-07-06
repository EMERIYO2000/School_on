from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    is_premium_subscriber = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username

class TutorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_profile'
    )
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255)
    certifications = models.TextField(blank=True, null=True)
    certificates_file = models.FileField(upload_to='media/certificates/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"Profil Pro de {self.user.username}"