from django.urls import path

from . import views
from gupb_queue import views as queue_views

urlpatterns = [
    path('<int:tournamentid>', views.tournament_details, name="Tournament Details"),
    path('all', views.tournaments, name="Tournaments"),
    path('add', views.tournament_add, name='Tournament Add'),
    path('<int:tournament_id>/queue/add', queue_views.add_queue_view, name='Add Queue')
]
