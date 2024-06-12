from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_action, name="login"),
    path('register', views.register_action, name="register"),
    path('logout', views.logout_action, name='logout'),
]