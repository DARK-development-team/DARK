from django.urls import path
from . import views

app_name = 'queue'
urlpatterns = [
    path('<int:queue_id>', views.show_queue_terms_view, name="Show Queue Terms"),
]
