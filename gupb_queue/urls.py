from django.urls import path
from . import views

app_name = 'gupb_queue'
urlpatterns = [
    path('<int:queue_id>', views.show_queue_terms_view, name="Show Queue Terms"),
    path('add/tournament/<int:tournament_id>', views.add_queue_view, name='Add Queue')
]
