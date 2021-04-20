from django.urls import path
from . import views

urlpatterns = [
    path('<int:roundid>', views.show_round_terms_view, name="Show Round Terms"),
    path('add', views.add_round_view, name="Add Round")
]
