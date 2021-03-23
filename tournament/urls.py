from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='Start-Page'),
    path('queuerequirements/<int:queueid>', views.queue_requirements, name="Queue-Requirements")
]
