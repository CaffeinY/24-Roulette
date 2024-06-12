from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/game/<int:gameID>', GameConsumer.as_asgi()),
]