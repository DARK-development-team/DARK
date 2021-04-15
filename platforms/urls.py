from django.urls import path
from . import views

app_name = 'platforms'
urlpatterns = [
    path('add', views.add_platform_view, name="Add Platform"),
    path('<int:platform_id>', views.platform_details_view, name="Platform Details"),
]
