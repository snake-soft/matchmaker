""" admin configuration for player module """
from django.contrib import admin
from django import forms
from .models import Player

# User permissions, Groups, Last login, First name, Last name, 

class PlayerAdmin(admin.ModelAdmin):
    #fields = ('username', 'name', 'is_staff', 'is_active', 'strength', 'email', )
    exclude = ('groups','permissions', 'user_permissions', 'date_joined', 'last_login')

admin.site.register(Player, PlayerAdmin)
