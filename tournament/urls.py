from django.urls import path
from . import views
from gupb_queue import views as queue_views


urlpatterns = [
    path('', views.start_page, name='Start-Page'),
    path('tournament/<int:tournament_id>', views.tournament_details, name="Tournament-Details"),
    path('tournaments', views.tournaments, name="Tournaments"),
    path('tournament/add', views.tournament_add, name='Tournament-Add'),
    path('tournament/<int:tournament_id>/queue<int:queue_id>', queue_views.queue_details, name="Queue-Details"),
]
