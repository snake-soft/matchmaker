""" admin configuration for player module """
from django.contrib import admin
from .models import Player


admin.site.register(Player)
