from django.contrib import admin
from django.urls import path, include, re_path
from .views import login, logout

urlpatterns = [
    path("login/", login),
    re_path(r'login/(\w+)/', login),
    path("logout/", logout),
]