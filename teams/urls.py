from django.urls import path
from teams.views import *

urlpatterns = [
    path('all', show_all_teams_view, name="Show All Teams"),
    path('<int:tournamentid>/all', show_all_tournament_teams_view, name="Show All Tournament Teams"),
    path('<int:userid>', show_user_teams_view, name="Show User Teams"),
]