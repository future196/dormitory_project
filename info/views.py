from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Building, Room, Check_in
from django.db.models import Q
from user.models import Student, Building_manager, Info_manager
import hashlib

def index(request):
    context = {
        'home': 0,
    }
    return render(request, "info_manager/index.html", context)


def building(request):
    dormitorys = Building.objects.all()
    context = {
        'dormitorys': dormitorys,
        'building': 0,
    }
    return render(request, "info_manager/building.html", context)


def add_building(request):
    if request.method == "POST":
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        height = request.POST.get("height")
        width = request.POST.get("width")
        room_capacity = request.POST.get("room_capacity")
        used = request.POST.get("used")
        obj = Building(name=name, height=height, width=width, capacity=capacity, room_capacity=room_capacity, used=used)
        obj.save()
        return redirect(building)

def check_exist(request, value):
    if Building.objects.filter(name=value):
        context = {
            'content': "1",
        }
        return JsonResponse(context)
    else:
        context = {
            'content': 0,
        }
        return JsonResponse(context)


def modify_building(request, name):
    dormitory = Building.objects.get(name=name)
    context = {
        'building': 0,
        'dormitory': dormitory,
    }
    return render(request, "info_manager/modify_building.html", context)

def change_building(request):
    if request.method == "POST":
        before_name = request.POST.get("before_name")
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        height = request.POST.get("height")
        width = request.POST.get("width")
        used = request.POST.get("used")
        room_capacity = request.POST.get("room_capacity")
        object = Building.objects.filter(name=before_name)[0]
        if before_name == name:
            object.capacity = capacity
            object.width = width
            object.height = height
            object.room_capacity = room_capacity
            object.used = used
            object.save()
        else:
            if Building.objects.filter(~Q(name=before_name), name=name):  # 排除等于before_id的值，查询是否有等于id的值
                context = {
                    'dormitory': {
                        'before_name': before_name,
                        'name': name,
                        'capacity': capacity,
                        'room_capacity': room_capacity,
                        'used': used,
                        'width': width,
                        'height': height,
                    },
                    'status': 1,
                }
                return render(request, "info_manager/modify_building.html", context)
            else:
                object.name=name
                object.capacity=capacity
                object.height=height
                object.width=width
                object.used=used
                object.room_capacity=room_capacity
                object.save()
        return redirect(building)


def delete_building(request,name):
    Building.objects.get(name=name).delete()
    return redirect(building)


def student(request, name, floor, number):
    building = Building.objects.all()
    if not Building.objects.filter(name=name):
        name = building[0]
    if number != "0" and len(number) == 1:
        number = "0" + number
    if floor == '0' and number == "0":
        string = name
        checkins = Check_in.objects.filter(room__name__startswith=string)
    elif floor == '0' and number != "0":
        string = name
        checkins = Check_in.objects.filter(room__name__startswith=string, room__name__endswith=number)
    elif floor != "0" and number == "0":
        string = name + floor
        checkins = Check_in.objects.filter(room__name__contains=string)
    else:
        string = name + floor + number
        checkins = Check_in.objects.filter(room__name=string)

    building_info = Building.objects.get(name=str(name))
    width = []
    for i in range(1, building_info.width + 1):
        if i < 10:
            width.append("0" + str(i))
        else:
            width.append(str(i))
    context = {
        'student': 0,
        'checkins': checkins,
        'name': name,
        'buildings': building,
        'building_height': range(1, building_info.height+1),
        'building_width': width,
        'floor': floor,
        'number': number,
    }
    return render(request, "info_manager/student.html", context)


def modify_student(request, id):
    checkin = Check_in.objects.get(id=id)
    date = str(checkin.date).split(" ")
    context = {
        'student': 0,
        'checkin': checkin,
        'date': date[0],
    }
    return render(request, "info_manager/modify_student.html", context)


def change_student(request, id):
    date = request.POST.get("date")
    status = request.POST.get("status")
    before_room = request.POST.get("before_room")
    room = request.POST.get("room")
    print(id, date, status, before_room, room)
    if before_room == room:
        checkin = Check_in.objects.get(id=id)
        checkin.date = date
        checkin.status = status
        checkin.save()
    else:
        obj = Room.objects.filter(name=room)
        if obj:
            if obj[0].capacity > 0:
                checkin = Check_in.objects.get(id=id)
                obj2 = Building.objects.get(name=room[0:2])
                checkin.date = date
                checkin.room = obj[0]
                checkin.building = obj2
                checkin.status = status
                checkin.save()
            else:
                context = {
                    'checkin': Check_in.objects.get(id=id),
                    'change_status': 'full',
                    'room': room,
                    'date': date,
                    'status': status,
                }
                return render(request, "info_manager/modify_student.html", context)
        else:
            context = {
                'checkin': Check_in.objects.get(id=id),
                'change_status': 'on_exist',
                'room': room,
                'date': date,
                'status': status,
            }
            return render(request, "info_manager/modify_student.html", context)


    return redirect("/info/student/A1/0/0/")


def find_student(request, student_id):
    student = Student.objects.filter(id=student_id)
    if student:
        checkin = Check_in.objects.filter(student__id=student[0].id)
        if checkin:
            date = str(checkin[0].date).split(" ")
            context = {
                "status": 0,
                "date": date[0],
                "id": student[0].id,
                "room": checkin[0].room.name,
                "name": student[0].name,
                "sex": student[0].sex,
                "class": student[0].class_grade,
                "checkin_status": checkin[0].status,
            }
        else:
            context = {
                "status": 1,
                "id": student[0].id,
                "name": student[0].name,
                "sex": student[0].sex,
                "class": student[0].class_grade,
            }
    else:
        context = {
            "status": 2,
        }
    return JsonResponse(context)


def find_room(request, room):
    room = Room.objects.filter(name=room)
    if room:
        if room[0].capacity > 0:
            context = {
                "status": 1,
            }
        else:
            context = {
                "status": 0,
            }
    else:
        context = {
            "status": 2,
        }
    return JsonResponse(context)


def add_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        room = request.POST.get("room")
        status = request.POST.get("status")
        date = request.POST.get("date")
        student = Student.objects.get(id=student_id)
        room = Room.objects.get(name=room)
        checkin = Check_in(student=student, room=room, status=status, date=date)
        checkin.save()
    return redirect("/info/student/A1/0/0/")


def manager(request):
    manager = Building_manager.objects.filter(building__name__contains="")
    context = {
        'manager': 0,
        'manager_info': manager,
        'buildings': Building.objects.all(),
    }
    return render(request, "info_manager/manager.html", context)


def find_manager(request, id):
    manager = Building_manager.objects.filter(id=id)
    if manager:
        try:
            print(manager[0].building.name)
            context = {
                "status": 0,
                "name": manager[0].name,
                "sex": manager[0].sex,
                "building": manager[0].building.name,
            }
        except:
            context = {
                "status": 1,
                "name": manager[0].name,
                "sex": manager[0].sex,
            }
    else:
        context = {
            "status": 2,
        }
    return JsonResponse(context)


def add_manager(request):
    if request.method == "POST":
        manager_id = request.POST.get("manager_id")
        building = request.POST.get("building")
        print(manager_id, building)
        obj = Building_manager.objects.get(id=manager_id)
        building = Building.objects.get(name=building)
        obj.building = building
        obj.save()
        return redirect(manager)


def modify_manager(request, id):
    manager_info = Building_manager.objects.get(id=id)
    context = {
        "manager": 0,
        "manager_info": manager_info,
        "buildings": Building.objects.all()
    }
    return render(request, "info_manager/modify_manager.html", context)


def change_manager(request, id):
    if request.method == "POST":
        building = request.POST.get("building")
        building = Building.objects.get(name=building)
        obj = Building_manager.objects.get(id=id)
        obj.building = building
        obj.save()
    return redirect(manager)



def modify_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        repeat_new_password = request.POST.get("repeat_password")
        if new_password == repeat_new_password:
            user_id = request.session["user_id"]
            obj = Info_manager.objects.get(id=user_id)
            if len(obj.password) < 20:
                pass
            else:
                m = hashlib.md5()
                m.update(bytes(password, encoding="utf-8"))
                password = m.hexdigest()
            m2 = hashlib.md5()
            m2.update(bytes(new_password, encoding="utf-8"))
            new_password = m2.hexdigest()
            if obj.password == password:
                obj.password = new_password
                obj.save()
                context = {
                    "modify_password": 0,
                    "status": 1,
                }
                return render(request, "info_manager/modify_password.html", context)
            else:
                context = {
                    "modify_password": 0,
                    "status": 0,
                }
                return render(request, "info_manager/modify_password.html", context)
        else:
            return HttpResponse("两次输入密码不一致！")
    else:
        context = {
            "modify_password": 0,
        }
        return render(request, "info_manager/modify_password.html", context)
