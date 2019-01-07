from django.shortcuts import render, HttpResponse, redirect
from .models import Info_manager, Student, Building_manager
import hashlib

def login(request, *type):
    if request.method == "GET":
        context = {
            'status': 0,
            'type': 0,
        }
        return render(request, "user/login.html", context)
    else:
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        context = {
            "user_id": user_id,
            "password": password,
        }
        m = hashlib.md5()
        m.update(bytes(password, encoding="utf-8"))
        hash_password = m.hexdigest()
        if type[0] == "info":
            context["type"] = 2
            obj = Info_manager.objects.filter(id=user_id)
            if obj:
                context["status"] = 1
                if len(obj[0].password) < 20:
                    if obj[0].password == password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "info"
                        return redirect("/info/index/")
                else:
                    if obj[0].password == hash_password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "info"
                        return redirect("/info/index/")
                return render(request, "user/login.html", context)
            else:
                context["status"] = 2
                return render(request, "user/login.html", context)
        elif type[0] == "student":
            context["type"] = 0
            obj = Student.objects.filter(id=user_id)
            if obj:
                context["status"] = 1
                if len(obj[0].password) < 20:
                    if obj[0].password == password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "student"
                        return redirect("/student/index/")
                else:
                    if obj[0].password == hash_password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "student"
                        return redirect("/student/index/")
                return render(request, "user/login.html", context)
            else:
                context["status"] = 2
                return render(request, "user/login.html", context)
        elif type[0] == "apartment":
            context["type"] = 1
            obj = Building_manager.objects.filter(id=user_id)
            if obj:
                context["status"] = 1
                if len(obj[0].password) < 20:
                    if obj[0].password == password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "apartment"
                        return redirect("/apartment/index/")
                else:
                    if obj[0].password == hash_password:
                        request.session["user_id"] = user_id
                        request.session["user_name"] = obj[0].name
                        request.session["user_type"] = "apartment"
                        return redirect("/apartment/index/")
                return render(request, "user/login.html", context)
            else:
                context["status"] = 2
                return render(request, "user/login.html", context)


def logout(request):
    del request.session["user_id"]
    del request.session["user_name"]
    del request.session["user_type"]
    return redirect(login)
