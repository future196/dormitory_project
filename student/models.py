from django.db import models

#
class Repair(models.Model):
    room = models.ForeignKey("info.Room", on_delete=models.CASCADE)
    student = models.ForeignKey("user.Student", on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="未处理")
    content = models.CharField(max_length=200, default="")
    contact = models.CharField(max_length=20, default="")
    reply = models.CharField(max_length=200, default="")
    wait = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.name
