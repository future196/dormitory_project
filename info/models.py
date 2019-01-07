from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=10, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    capacity = models.IntegerField()
    used = models.IntegerField(null=False, default=0)
    room_capacity = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=10, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Check_in(models.Model):
    student = models.ForeignKey("user.Student", on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=5, default="")

    def __str__(self):
        return self.student

