from django.urls import path
from . import views

urlpatterns = [
    path('<int:tournamentid>', views.tournament_details, name="Tournament Details"),
    path('all', views.tournaments, name="Tournaments"),
    path('add', views.tournament_add, name='Tournament Add'),
]
