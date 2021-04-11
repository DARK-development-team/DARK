from django.urls import path
from teams.views import *

urlpatterns = [
    path('all', show_all_teams_view, name="Show All Teams"),
    path('<slug:username>', show_user_teams_view, name="Show User Teams"),
]
