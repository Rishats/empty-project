from django.contrib import admin

from .models import Student
from .models import Work

admin.site.register(Student)
admin.site.register(Work)