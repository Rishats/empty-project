from django.contrib import admin

from .models import Student
from .models import Work
from .models import PasswordDatabase

admin.site.register(Student)
admin.site.register(Work)
admin.site.register(PasswordDatabase)