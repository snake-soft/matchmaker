from django.urls import path
from .views import OverviewTeamPlayer

urlpatterns = [
    path('overview/', OverviewTeamPlayer.as_view()),
]
