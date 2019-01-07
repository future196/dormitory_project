from django.contrib import admin
from apartment.models import *
from info.models import *
from user.models import *
from student.models import *

# Register your models here.

admin.site.register([Cost, Entry_exit])
admin.site.register([Building, Room, Check_in])
admin.site.register(Repair)
admin.site.register([Building_manager, Student, Info_manager])

