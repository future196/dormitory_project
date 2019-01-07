from django.http import JsonResponse
import hashlib
from user.models import Student
from info.models import Room, Check_in
from apartment.models import Cost
from student.models import Repair
# Create your views here.


def login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("user_password")
        m = hashlib.md5()
        m.update(bytes(password, encoding="utf-8"))
        hash_password = m.hexdigest()
        context = {

        }
        obj = Student.objects.filter(id=user_id)
        if obj:
            if len(obj[0].password) < 20:
                if obj[0].password == password:
                    context["status"] = 1
                    request.session["user_id"] = user_id
                    return JsonResponse(context)
                context["status"] = 2
            else:
                if obj[0].password == hash_password:
                    context["status"] = 1
                    request.session["user_id"] = user_id
                    return JsonResponse(context)
                context["status"] = 2
            return JsonResponse(context)
        else:
            context["status"] = 3
            return JsonResponse(context)


def index(request, user_id):
    student = Student.objects.get(id=user_id)
    checkin = Check_in.objects.filter(student__id=user_id)
    context = {
        "student_id": user_id,
        "student_name": student.name,
        "student_sex": student.sex,
        "student_class": student.class_grade,
    }
    if checkin:
        context["student_room"] = checkin[0].room.name
    else:
        context["student_room"] = "未入住"
    return JsonResponse(context)


def cost(request, user_id):
    checkin = Check_in.objects.get(student__id=user_id)
    costs = Cost.objects.filter(room__name=checkin.room.name).order_by("-date")
    context = []
    for cost in costs:
        context.append({
            "date": cost.date,
            "room": cost.room.name,
            "water": cost.water,
            "electric": cost.electric,
            "water_status": cost.water_status,
            "electric_status": cost.electric_status,
        })
    return JsonResponse(context, safe=False)


def repair(request, user_id):
    if request.method == "POST":
        checkin = Check_in.objects.filter(student__id=user_id)
        if checkin:
            student = Student.objects.get(id=user_id)
            room = Room.objects.get(id=checkin[0].room.id)
            type = request.POST.get("repair_type")
            content = request.POST.get("repair_content")
            contact = request.POST.get("repair_contact")
            name = request.POST.get("repair_name")
            obj = Repair(room=room, student=student, type=type, content=content, contact=contact, name=name)
            obj.save()
            context = {
                "status": 1,
            }
        else:
            context = {
                "status": 2,
            }
        return JsonResponse(context)
    else:
        repairs = Repair.objects.filter(student__id=user_id).order_by("-date")
        context = []
        for repair in repairs:
            context.append({
                "room": repair.room.name,
                "type": repair.type,
                "name": repair.name,
                "date": repair.date,
                "status": repair.status,
                "content": repair.content,
                "contact": repair.contact,
            })
        return JsonResponse(context, safe=False)



def change_password(request, user_id):
    if request.method == "POST":
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
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
                "status": 1,
            }
            return JsonResponse(context)
        else:
            context = {
                "status": 2,
            }
            return JsonResponse(context)


