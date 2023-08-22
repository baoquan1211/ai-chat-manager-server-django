from django.urls import path

from .views import app

urlpatterns = [
    path("/socket.io/", app),
]
