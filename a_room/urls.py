from django.urls import path
from a_room import views

urlpatterns = [
    path('', views.getLobbyView, name='lobby'),
    path('join-room/<int:roomID>', views.joinRoom, name='joinRoom'),
    path('exit-room/<int:roomID>', views.exitRoom, name='exitRoom'),
    path('start/<int:roomID>', views.start_game, name="start"),
]