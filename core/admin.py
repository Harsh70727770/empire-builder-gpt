from django.contrib import admin
from .models import StartupIdea, UserProfile

# Register your models here.
admin.site.register(StartupIdea)
admin.site.register(UserProfile)