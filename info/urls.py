from django.urls import path, re_path
from info.views import index, building, add_building, check_exist, modify_building,\
    change_building, delete_building, student, modify_student, change_student,find_student,\
    add_student, find_room, manager, find_manager, add_manager, modify_manager, change_manager,\
    modify_password



urlpatterns = [
    path("index/", index),

    path("building/", building),
    path("building/add/", add_building),
    re_path("building/check_exist_(\w+)", check_exist),
    re_path("building/modify/(\w+)/", modify_building),
    path("building/change/", change_building),
    re_path("building/delete/(\w+)/", delete_building),

    re_path("student/(\w+)/(\w+)/(\w+)/", student),
    re_path("student/modify/(\w+)/", modify_student),
    re_path('student/change/(\w+)/', change_student),
    re_path("student/find_student/(\d+)/", find_student),
    re_path("student/find_room/(\w+)/", find_room),
    path("student/add/", add_student),

    path("manager/", manager),
    re_path("manager/find_manager/(\d+)/", find_manager),
    path("manager/add/", add_manager),
    re_path("manager/modify/(\d+)/", modify_manager),
    re_path("manager/change/(\d+)/", change_manager),

    path("modify_password/", modify_password),
]