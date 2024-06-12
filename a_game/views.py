from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.dateparse import parse_datetime
from .models import Game
from a_room.models import Room 
import random
import string
import json
import time

# Create your views here.
@ensure_csrf_cookie
def gameHomePage(request):
    return render(request, 'home.html')

@ensure_csrf_cookie
def showRulePage(request):
    return render(request, 'rule.html')



@login_required
def getGameView(request, roomID):
    room = get_object_or_404(Room, id=roomID)
    if not room.game.exists():
        return Http404  
    
    
    game = get_object_or_404(Game, room=room)

    context = {
        'game': game,
        'user': request.user,
    }

    return render(request, 'game.html', context)