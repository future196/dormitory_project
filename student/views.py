from django.shortcuts import render, HttpResponse, redirect
from student.models import Repair
from info.models import Check_in, Room
from user.models import Student
from apartment.models import Cost
import hashlib


def index(request):
    context = {
        "home": 0,
    }
    return render(request, "student/index.html", context)

def repair(request):
    repairs = Repair.objects.filter(student__id=request.session["user_id"]).order_by("-date")
    checkin = Check_in.objects.filter(student__id=request.session["user_id"])
    if checkin:
        context = {
            "repair": 0,
            "repairs": repairs,
            "ischeckin": 0,
        }
    else:
        context = {
            "repair": 0,
            "repairs": repairs,
        }
    return render(request, "student/repair.html", context)


def check_repair(request,id):
    repair = Repair.objects.get(id=id)
    repair.wait = "已确认验收"
    print("23213123")
    repair.save()
    return redirect("/student/repair")


def repair_reply(request, id):
    content = request.POST.get("content")
    repair = Repair.objects.get(id=id)
    repair.wait = "已反馈"
    repair.reply = content
    repair.save()
    return redirect("/student/repair")


def add_repair(request, room):
    if request.method == "GET":
        context = {
            "repair": 0,
            "room": Check_in.objects.get(student__id=request.session["user_id"]).room.name,
        }
        return render(request, "student/add_repair.html", context)
    elif request.method == "POST":
        type = request.POST.get("type")
        name = request.POST.get("name")
        content = request.POST.get("content")
        contact = request.POST.get("contact")
        student = Student.objects.get(id=request.session["user_id"])
        room = Room.objects.get(name=room)
        obj = Repair(room=room, student=student, type=type, name=name, content=content, contact=contact)
        obj.save()
        return redirect(repair)


def cost(request):
    user_id = request.session["user_id"]
    checkin = Check_in.objects.filter(student__id=user_id)
    context = {
        "cost": 0,
    }
    if checkin:
        costs = Cost.objects.filter(room__name=checkin[0].room.name).order_by("-date")
        context["costs"] = costs
    return render(request, "student/cost.html", context)


def cost_pay(request, type, id):
    cost = Cost.objects.get(id=id)
    if int(type) == 1:
        cost.water_status = "已缴纳"
    else:
        cost.electric_status = "已缴纳"
    cost.save()
    return redirect("/student/cost")

def modify_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        repeat_new_password = request.POST.get("repeat_password")
        if new_password == repeat_new_password:
            user_id = request.session["user_id"]
            obj = Student.objects.get(id=user_id)
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
                return render(request, "student/modify_password.html", context)
            else:
                context = {
                    "modify_password": 0,
                    "status": 0,
                }
                return render(request, "student/modify_password.html", context)
        else:
            return HttpResponse("两次输入密码不一致！")
    else:
        context = {
            "modify_password": 0,
        }
        return render(request, "student/modify_password.html", context)
