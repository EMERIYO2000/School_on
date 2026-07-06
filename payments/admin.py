from django.contrib import admin
from .models import Payments
# Register your models here.

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'student', 'course', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'student__username', 'course__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)