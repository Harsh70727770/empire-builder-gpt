from django.contrib import admin
from .models import StartupIdea, UserProfile, ContactMessage

# Register your models here.
admin.site.register(StartupIdea)
admin.site.register(UserProfile)
admin.site.register(ContactMessage)