"""ranker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from core.views import StartView
from core.views import DateSetView
from player.views import PlayerDetails, PlayerCreate
from team.views import TeamList, TeamDetails, TeamCreate, TeamListRealtime
from match.views import MatchList, MatchDetails, MatchCreate
from matchmaker.views import MatchmakerView
from account.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(
        template_name='account/signup.html',), name='signup'),

    path('login/', LoginView.as_view(
        template_name='account/login.html',), name='login'),

    path('logout/', LogoutView.as_view(
        template_name='account/logout.html',), name='logout'),


    path('', StartView.as_view(), name="home"),
    path('set/date/', DateSetView.as_view(), name="set-date"),
    path('balancer/', MatchmakerView.as_view(), name="matchmaker"),

    # path('player/', PlayerList.as_view(), name='player-list'),
    path('player/<pk>/', PlayerDetails.as_view(), name="player-details"),
    path('new/player/', PlayerCreate.as_view(), name="player-new"),

    path('team/', TeamList.as_view(), name="team-list"),
    path('ladder/', TeamList.as_view(), name="ladder"),
    path('team/<pk>/', TeamDetails.as_view(), name="team-details"),
    path('new/team/', TeamCreate.as_view(), name="team-new"),
    path('realtime/team/', TeamListRealtime.as_view(), name="team-realtime"),

    path('match/', MatchList.as_view(), name="match-list"),
    path('match/<pk>/', MatchDetails.as_view(), name="match-details"),
    path('tracker/', MatchCreate.as_view(), name="match-new"),
]
