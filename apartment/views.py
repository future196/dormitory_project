from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from info.models import Room, Building, Check_in
from user.models import Building_manager, Student
from student.models import Repair
from apartment.models import Cost, Entry_exit
import datetime
import hashlib



def index(request):
    context = {
        "home": 0,
    }
    return render(request, "apartment_manager/index.html", context)


def room(request, floor):
    # 宿舍批量添加程序
    # print("开始执行")
    # building = Building.objects.get(name="D3")
    # num = 0
    # id = 701
    # while num < 30:
    #     room = Room(name="D3" + str(id), capacity=4, building=building)
    #     room.save()
    #     print("添加成功", id)
    #     num = num + 1
    #     id = id + 1

    user_id = request.session["user_id"]
    manager = Building_manager.objects.get(id=user_id)
    building = manager.building.name
    string = str(building)+str(floor)
    rooms = Room.objects.filter(name__contains=string)
    context = {
        "floor": floor,
        "rooms": rooms,
        "room": 0,
        "height": range(1, manager.building.height+1),
    }
    return render(request, "apartment_manager/room.html", context)


def room_detail(request, room):
    checkins = Check_in.objects.filter(room__name=room)
    context = {
        "room": 0,
        "checkins": checkins,
        "room_info": Room.objects.get(name=room),
        "num": len(checkins)
    }
    return render(request, "apartment_manager/room_detail.html", context)



def remove_checkin(request, id, room):
    Check_in.objects.get(id=id).delete()
    obj = Room.objects.get(name=room)
    obj.used = obj.used - 1
    obj.capacity = obj.capacity + 1
    obj.save()
    return redirect("/apartment/room/detail/%s/" % room)



def find_student(request, student_id):
    student = Student.objects.filter(id=student_id)
    if student:
        checkin = Check_in.objects.filter(student__id=student[0].id)
        if checkin:
            date = str(checkin[0].date).split(" ")
            context = {
                "status": 0,
                "id": student[0].id,
                "name": student[0].name,
                "sex": student[0].sex,
                "class": student[0].class_grade,
                "room": checkin[0].room.name,
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


def checkin(request, room):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        room = Room.objects.get(name=room)
        checkin= Check_in(student=Student.objects.get(id=student_id), room=room, status="是")
        checkin.save()
        room.used = room.used + 1
        room.capacity = room.capacity - 1
        room.save()
        return redirect("/apartment/room/detail/%s/" % room)
    return HttpResponse("不是post方法或未知错误！")



def student(request, floor, num, search):
    user_id = request.session["user_id"]
    manager = Building_manager.objects.get(id=user_id)
    if str(floor) == "0" and str(num) == "0":
        string = manager.building.name
        checkins = Check_in.objects.filter(room__name__startswith=string)
    elif str(floor) == "0" and str(num) != "0":
        if int(num) < 10:
            num = "0" + str(num)
        string = manager.building.name
        checkins = Check_in.objects.filter(room__name__startswith=string, room__name__endswith=num)
    elif str(floor) != "0" and str(num) != "0":
        if int(num) < 10:
            num = "0" + str(num)
        string = str(manager.building.name)+str(floor)+str(num)
        checkins = Check_in.objects.filter(room__name=string)
    elif str(floor) != "0" and str(num) == "0":
        if int(num) < 10:
            num = "0" + str(num)
        string = str(manager.building.name)+str(floor)
        checkins = Check_in.objects.filter(room__name__contains=string)
    if search != "search":
        checkins = Check_in.objects.filter(student__id__contains=search)
    width = []
    for i in range(1, manager.building.width + 1):
        if i < 10:
            width.append("0" + str(i))
        else:
            width.append(str(i))
    context = {
        "string": string[:2],
        "student": 0,
        "checkins": checkins,
        "building_height": range(1, manager.building.height+1),
        "building_width": width,
        "floor": int(floor),
        "num": int(num),
    }

    return render(request, "apartment_manager/student.html", context)


def repair(request, status):
    if status == "0":
        building = Building_manager.objects.get(id=request.session["user_id"]).building.name
        repairs = Repair.objects.filter(room__name__startswith=building).order_by("-date")
        waits = Repair.objects.filter(room__name__startswith=building, status="未处理")
        context = {
            "repair": 0,
            "repairs": repairs,
            'wait': len(waits),
            "status": status,
        }
        return render(request, "apartment_manager/repair.html", context)
    elif status == "2":
        building = Building_manager.objects.get(id=request.session["user_id"]).building.name
        waits = Repair.objects.filter(room__name__startswith=building, status="未处理").order_by("-date")
        context = {
            "repair": 0,
            "repairs": waits,
            'wait': len(waits),
            "status": status,
        }
        return render(request, "apartment_manager/repair.html", context)


def repair_finish(request, id, status):
    repair = Repair.objects.get(id=id)
    repair.status = "已处理"
    repair.wait = "等待确认验收"
    repair.save()
    return redirect("/apartment/repair/%s/" % status)


def cost(request, type, year, month):
    user_id = request.session["user_id"]
    if type == "0" and year == "0" and month == "0":
        room_name = Building_manager.objects.get(id=user_id).building.name
        costs = Cost.objects.filter(room__name__startswith=room_name).order_by("-date")
    elif type != "0" and year == "0" and month == "0":
        if type == "1":
            costs = Cost.objects.filter(water_status="未缴纳").order_by("-date")
        elif type == "2":
            costs = Cost.objects.filter(electric_status="未缴纳").order_by("-date")
        elif type == "3":
            costs = Cost.objects.filter(water_status="已缴纳").order_by("-date")
        elif type == "4":
            costs = Cost.objects.filter(electric_status="已缴纳").order_by("-date")
    elif type == "0" and year != "0" and month == "0":
        costs = Cost.objects.filter(date__startswith=year).order_by("-date")
    elif type == "0" and year == "0" and month != "0":
        costs = Cost.objects.filter(date__endswith=month+"月").order_by("-date")
    elif type == "0" and year != "0" and month != "0":
        costs = Cost.objects.filter(date__startswith=year, date__endswith=month + "月").order_by("-date")
    elif type != "0" and year != "0" and month == "0":
        if type == "1":
            costs = Cost.objects.filter(electric_status="未缴纳", date__startswith=year).order_by("-date")
        elif type == "2":
            costs = Cost.objects.filter(electric_status="未缴纳", date__startswith=year).order_by("-date")
        elif type == "3":
            costs = Cost.objects.filter(electric_status="已缴纳", date__startswith=year).order_by("-date")
        elif type == "4":
            costs = Cost.objects.filter(electric_status="已缴纳", date__startswith=year).order_by("-date")
    elif type != "0" and year != "0" and month != "0":
        if type == "1":
            costs = Cost.objects.filter(electric_status="未缴纳", date__startswith=year, date__endswith=month + "月").order_by("-date")
        elif type == "2":
            costs = Cost.objects.filter(electric_status="未缴纳", date__startswith=year, date__endswith=month + "月").order_by("-date")
        elif type == "3":
            costs = Cost.objects.filter(electric_status="已缴纳", date__startswith=year, date__endswith=month + "月").order_by("-date")
        elif type == "4":
            costs = Cost.objects.filter(electric_status="已缴纳", date__startswith=year, date__endswith=month + "月").order_by("-date")

    context = {
        "cost": 0,
        "costs": costs,
        "type": type,
        "year": year,
        "month": month,
    }
    return render(request, "apartment_manager/cost.html", context)


def modify_cost(request, id, type, year, month):
    cost_info = Cost.objects.get(id=id)
    context = {
        "cost": 0,
        "cost_info": cost_info,
        "type": type,
        "year": year,
        "month": month,
    }
    return render(request, "apartment_manager/modify_cost.html", context)


def change_cost(request, id, type, year, month):
    cost = Cost.objects.get(id=id)
    water_status = request.POST.get("water_status")
    electric_status = request.POST.get("electric_status")
    cost.water_status = water_status
    cost.electric_status = electric_status
    cost.save()
    return redirect("/apartment/cost/%s_%s_%s/" % (type, year, month))


def add_cost(request):
    user_id = request.session["user_id"]
    manager = Building_manager.objects.get(id=user_id)
    if request.method == "POST":
        now_time = datetime.datetime.now()
        floor = request.POST.get("floor")
        num = request.POST.get("room")
        if int(num[0:-2]) < 10:
            num = "0" + num[0:-2]
        else:
            num = num[0:-2]
        month = request.POST.get("month")
        date = str(now_time)[0:4] + "年" + month
        room = manager.building.name + floor[0:-1] + num
        water = request.POST.get("water")
        electric = request.POST.get("electric")
        cost = Cost(water=water, electric=electric, date=date, room=Room.objects.get(name=room))
        cost.save()
        return redirect("/apartment/cost/0_0_0/")
    else:
        width = []
        for i in range(1, manager.building.width + 1):
            if i < 10:
                width.append("0" + str(i))
            else:
                width.append(str(i))
        context = {
            "cost": 0,
            "height": range(1, manager.building.height+1),
            "width": width,
            "building_name": manager.building.name,
        }
        return render(request, "apartment_manager/add_cost.html", context)


def entry_exit(request, type, year, month):
    user_id = request.session["user_id"]
    if type == "0" and year == "0" and month == "0":
        manager = Building_manager.objects.get(id=user_id)
        entry_exits = Entry_exit.objects.filter(building__name=manager.building.name).order_by("-date")
    elif type != "0" and year == "0" and month == "0":
        if type == "1":
            entry_exits = Entry_exit.objects.filter(status="出").order_by("-date")
        elif type == "2":
            entry_exits = Entry_exit.objects.filter(status="入").order_by("-date")
    elif type == "0" and year != "0" and month == "0":
        entry_exits = Entry_exit.objects.filter(date__startswith=year).order_by("-date")
    elif type == "0" and year == "0" and month != "0":
        if int(month) < 10:
            month = "0" + str(month)
        string = "-" + str(month) + "-"
        entry_exits = Entry_exit.objects.filter(date__contains=string).order_by("-date")
    elif type == "0" and year != "0" and month != "0":
        if int(month) < 10:
            month = "0" + str(month)
        string = "-" + str(month) + "-"
        entry_exits = Entry_exit.objects.filter(date__startswith=year, date__contains=string).order_by("-date")
    elif type != "0" and year != "0" and month == "0":
        if type == "1":
            entry_exits = Entry_exit.objects.filter(status="出", date__startswith=year).order_by("-date")
        elif type == "2":
            entry_exits = Entry_exit.objects.filter(status="入", date__startswith=year).order_by("-date")
    elif type != "0" and year != "0" and month != "0":
        if int(month) < 10:
            month = "0" + str(month)
        string = "-" + str(month) + "-"
        if type == "1":
            entry_exits = Entry_exit.objects.filter(electric_status="出", date__startswith=year, date__contains=string).order_by("-date")
        elif type == "2":
            entry_exits = Entry_exit.objects.filter(electric_status="入", date__startswith=year, date__contains=string).order_by("-date")

    context = {
        "entry_exit": 0,
        "entry_exits": entry_exits,
        "type": type,
        "year": year,
        "month": month,
    }
    return render(request, "apartment_manager/entry_exit.html", context)


def add_entry_exit(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        manager = Building_manager.objects.get(id=user_id)
        student_id = request.POST.get("student_id")
        name = request.POST.get("name")
        status = request.POST.get("status")
        entry_exit = Entry_exit(student=Student.objects.get(id=student_id), name=name, status=status, building=Building.objects.get(name=manager.building.name))
        entry_exit.save()
        return redirect("/apartment/entry_exit/0_0_0/")
    else:
        context = {
            "entry_exit": 0,
        }
        return render(request, "apartment_manager/add_entry_exit.html", context)


def modify_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        repeat_new_password = request.POST.get("repeat_password")
        if new_password == repeat_new_password:
            user_id = request.session["user_id"]
            obj = Building_manager.objects.get(id=user_id)
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
                return render(request, "apartment_manager/modify_password.html", context)
            else:
                context = {
                    "modify_password": 0,
                    "status": 0,
                }
                return render(request, "apartment_manager/modify_password.html", context)
        else:
            return HttpResponse("两次输入密码不一致！")
    else:
        context = {
            "modify_password": 0,
        }
        return render(request, "apartment_manager/modify_password.html", context)


def device_management(request):
    context = {
        "device_management": 0,
    }
    return render(request, "apartment_manager/device_management.html", context)


