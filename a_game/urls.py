from django.urls import path
from a_game import views

urlpatterns = [
    path('join-game/<int:roomID>', views.getGameView, name='join-game'),
]