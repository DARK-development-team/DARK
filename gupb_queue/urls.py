from django.urls import path
from . import views

app_name = 'gupb_queue'
urlpatterns = [
    path('tournament/<int:tournament_id>/queue<int:queue_id>', views.queue_details, name="Queue-Details"),
    path('tournament/<int:tournament_id>/queue/add', views.queue_add, name='Queue-Add')
]
