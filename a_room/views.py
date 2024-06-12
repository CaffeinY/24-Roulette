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
from .models import Room
import random
import string
import json
import time


# Create your views here.
@login_required
@ensure_csrf_cookie
def getLobbyView(request):
    # get all rooms
    rooms = Room.objects.all()
    context = {
        "rooms": rooms
    }
    
    
    return render(request, 'lobby.html', context)

@login_required
@ensure_csrf_cookie
def joinRoom(request, roomID):
    pass


@login_required
@ensure_csrf_cookie
def exitRoom(request, roomID):
    pass



@login_required
@ensure_csrf_cookie
def start_game(request, roomID):
    pass