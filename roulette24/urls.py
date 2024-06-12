"""roulette24 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from a_game import views as game_views
from a_user import views as user_views
from a_room import views as room_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('a_user.urls')),
    path('lobby/', include('a_room.urls')),
    path('rule', game_views.showRulePage, name='rule'),
    path('game/', include('a_game.urls')),
    path('' , game_views.gameHomePage, name='home'),
]
