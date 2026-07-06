from django.db import models
from django.conf import settings

# Create your models here.
class Booking(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'En attente de confirmation'),
        ('accepted', 'Accepté par le professeur'),
        ('rejected', 'Rejeté par le professeur'),
        ('completed', 'Session terminée'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    tutor = models.ForeignKey('utilisateurs.TutorProfile', on_delete=models.CASCADE, related_name='tutor_bookings')
    date_requested = models.DateField() # Date du cours demandé
    time_requested = models.TimeField() # Heure d'enseignement du cours
    adress = models.CharField(max_length=255) # Adresse du quartier d'un etudition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Réservation de {self.student.username} chez {self.tutor.user.username}"
    
