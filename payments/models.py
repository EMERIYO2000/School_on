from django.db import models
from django.conf import settings
# Create your models here.

class Payments(models.Model):
    
    PAYMENT_STATUS = [
        ('pending', 'En attente'),
        ('completed', 'Payé avec succès'),
        ('failed', 'Échec de la transaction'),
    ]
    PAYMENT_METHODS = [
        ('lumicash', 'Lumicash'),
        ('eco_cash', 'EcoCash'),
        ('bank_transfer', 'Virement bancaire'),
        ('bitcoin', 'Bitcoin (Lightning Network)'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='lumicash')
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction {self.transaction_id} le {self.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.amount}"
    