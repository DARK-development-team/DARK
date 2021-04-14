from django.urls import path, include

from . import views
from round import views as round_views

urlpatterns = [
    path('<int:tournamentid>', views.tournament_details, name="Tournament Details"),
    path('all', views.tournaments, name="Tournaments"),
    path('add', views.tournament_add, name='Tournament Add'),
    path('<int:tournamentid>/round/', include('round.urls')),
]
