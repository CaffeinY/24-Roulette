from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/lobby/', LobbyConsumer.as_asgi()),
]
