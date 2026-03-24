# login/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Azubi

# Registriere das benutzerdefinierte Benutzermodell
admin.site.register(Azubi, UserAdmin)
