from django.urls import path
from dark.home.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='Home Page'),
    path('index', HomePageView.as_view(), name='Home Page'),
]
