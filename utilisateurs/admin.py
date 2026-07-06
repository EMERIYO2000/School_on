from django.contrib import admin
from .models import CustomUser, TutorProfile
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(TutorProfile)