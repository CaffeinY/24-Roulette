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
from a_user.forms import *
import random
import string
import json
import time


# Create your views here.
@ensure_csrf_cookie
def login_action(request):
    context = {}
    if request.method == "GET":
        context['form'] = LoginForm()
        return render(request, 'login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'login.html', context)
    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    login(request, new_user)

    return redirect(reverse('home'))



@ensure_csrf_cookie
def register_action(request):
    context = {}
    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)


    form = RegisterForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'register.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        )
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)

    # also create a custom_user object in db
    new_profile = Profile(user=request.user,
                          in_game=False,
                          is_ready=False,
                          win=0,
                          lose=0,
                          chips=0,)
    new_profile.save()

    return redirect(reverse('home'))


@login_required
@ensure_csrf_cookie
def logout_action(request):
    logout(request)
    return redirect(reverse('home'))
