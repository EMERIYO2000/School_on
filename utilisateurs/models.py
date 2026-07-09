from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Adresse Email')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_teacher = models.BooleanField(default=False)
    is_premium_subscriber = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.email}"

class TutorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_profile'
    )
    bio = models.TextField(blank=True, null=True,verbose_name="Biographie")
    skills = models.CharField(
        max_length=255,
        verbose_name="Compétences",
        help_text="Compétences séparées par des virgules (ex: Python, Design, Réseaux)."
    )
    
    certifications = models.TextField(blank=True, null=True)
    certificates_file = models.FileField(upload_to='media/certificates/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(
        max_length=100, 
        blank=True, 
        default="Burundi",  # Optionnel : tu peux définir un pays par défaut
        verbose_name="Pays"
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Ville"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Vérifie par l'équipe")
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"Profil Mentor - {self.user.get_full_name()} ({self.city}, {self.country})"