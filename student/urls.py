from django.urls import path, re_path
from student.views import index, repair, add_repair, modify_password, cost, cost_pay, check_repair, repair_reply

urlpatterns = [
    path("index/", index),
    path("repair/", repair),
    re_path("repair/add/(\w+)/", add_repair),
    path("cost/", cost),
    path("modify_password/", modify_password),
    re_path("cost/pay/(\d+)/(\d+)", cost_pay),
    re_path("check_repair/(\d+)", check_repair),
    re_path("repair_reply/(\d+)", repair_reply),
]