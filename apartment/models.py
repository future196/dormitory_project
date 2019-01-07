from django.db import models


class Cost(models.Model):
    room = models.ForeignKey("info.Room", on_delete=models.CASCADE)
    water = models.DecimalField(max_digits=10, decimal_places=2)
    electric = models.DecimalField(max_digits=10, decimal_places=2)
    water_status = models.CharField(max_length=10, default="未缴纳")
    electric_status = models.CharField(max_length=10, default="未缴纳")
    date = models.CharField(max_length=20)

    def __str__(self):
        return self.room

class Entry_exit(models.Model):
    student = models.ForeignKey("user.Student", on_delete=models.CASCADE)
    building = models.ForeignKey("info.Building", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.student