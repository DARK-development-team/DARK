from django.urls import path
from bots.views import *

urlpatterns = [
    path('', show_team_bots_view, name="Show Team Bots"),
    path('<int:botid>', manage_team_round_bot_view, name="Manage Bot"),
    path('<int:botid>/remove', remove_team_round_bot_view, name="Remove Bot"),
    path('add/<int:roundid>', add_team_bot_round_view, name="Add Bot"),
]