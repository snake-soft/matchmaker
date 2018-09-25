""" admin configuration for team model """
from django.contrib import admin
from .models import Team
from player.models import Player

admin.site.register(Team)

#===============================================================================
# class TeamPlayerInline(admin.TabularInline):
#     model = Team.players.through
# 
# class TeamPlayerAdmin(admin.ModelAdmin):
#     inlines = [TeamPlayerInline]
# 
# 
# admin.site.register(Player, TeamPlayerAdmin)
#===============================================================================
