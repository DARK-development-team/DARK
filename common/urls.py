from django.urls import path
from common.views import start_page

urlpatterns = [
    path('', start_page, name='Start Page'),
]
