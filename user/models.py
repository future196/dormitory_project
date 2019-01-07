from django.db import models

class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=6)
    password = models.CharField(max_length=50)
    class_grade = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Building_manager(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=6)
    password = models.CharField(max_length=50)
    building = models.ForeignKey("info.Building", on_delete=models.CASCADE,  null=False)

    def __str__(self):
        return self.name

class Info_manager(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=6)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name