from django.contrib import admin

from .models import Community, CommunityMembership


class CommunityInline(admin.TabularInline):
    model = CommunityMembership


class CommunityAdmin(admin.ModelAdmin):
    inlines = [CommunityInline]


admin.site.register(Community, CommunityAdmin)
