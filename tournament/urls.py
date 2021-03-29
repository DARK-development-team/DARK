from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='Start-Page'),
    path('tournament/<int:tournament_id>', views.tournament_details, name="Tournament-Details"),
    path('tournaments', views.tournaments, name="Tournaments"),
]
