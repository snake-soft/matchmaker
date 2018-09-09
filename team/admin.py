""" admin configuration for team model """
from django.contrib import admin
from .models import Team


admin.site.register(Team)
