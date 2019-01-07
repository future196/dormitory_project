from django.urls import path, re_path
from mobile.views import login, index, cost, repair, change_password
urlpatterns = [
    path("login/", login),
    re_path("index/(\w+)/", index),
    re_path("cost/(\w+)/", cost),
    re_path("repair/(\w+)/", repair),
    re_path("change_password/(\w+)/", change_password),
]