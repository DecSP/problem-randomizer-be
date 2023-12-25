from django.urls import path

from .websocket import WSConsumer

websocket_urlpatterns = [
    path("ws/", WSConsumer.as_asgi()),
]
