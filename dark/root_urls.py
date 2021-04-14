from django.contrib import admin
from django.urls import path

from .urls import home, user, tournament

urlpatterns = [
    path('', home.site.urls),
    path('user/', user.site.urls),
    path('admin/', admin.site.urls),
    path('tournaments/', tournament.site.urls),
]
