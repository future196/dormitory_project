from django.urls import path, re_path
from apartment.views import index, room, room_detail, find_student, checkin, student, repair, repair_finish,\
    cost, modify_cost, change_cost, add_cost, entry_exit, add_entry_exit, modify_password, remove_checkin,\
    device_management

urlpatterns = [
    path('index/', index),

    re_path('room/(\d+)/', room),
    re_path('room/detail/(\w+)/', room_detail),
    re_path('room/find_student/(\d+)/', find_student),
    re_path('room/checkin/(\w+)/', checkin),
    re_path('room/remove/(\w+)/(\w+)/', remove_checkin),

    re_path('student/(\d+)/(\d+)/(\w+)', student),

    re_path("repair/(\w+)/", repair),
    re_path('repair_finish/(\d+)/(\d+)/', repair_finish),

    re_path("cost/(\w+)_(\w+)_(\w+)/", cost),
    re_path("cost/modify/(\w+)/(\w+)_(\w+)_(\w+)/", modify_cost),
    re_path("cost/change/(\w+)/(\w+)_(\w+)_(\w+)/", change_cost),
    path("cost/add/", add_cost),

    re_path("entry_exit/(\w+)_(\w+)_(\w+)/", entry_exit),
    path("entry_exit/add/", add_entry_exit),
    re_path("entry_exit/add/find_student/(\d+)/", find_student),

    path("device/", device_management),

    path("modify_password/", modify_password),
]