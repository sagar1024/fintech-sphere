# Register your models here.

# users/admin.py
from django.contrib import admin
from .models import Profile, Investment

admin.site.register(Profile)
admin.site.register(Investment)
