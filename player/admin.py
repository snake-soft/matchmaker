""" admin configuration for player module """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Player


admin.site.register(Player)
