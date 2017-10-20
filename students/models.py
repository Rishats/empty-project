from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.db import connection


class Student(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField('Datetime created')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
# Dev
def create_profile_database(sender, **kwargs):
    if kwargs['created']:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE go")
            row = cursor.fetchone()
        return row

post_save.connect(create_profile_database, sender=Student)

class Work(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=255, blank=True)
    points = models.PositiveSmallIntegerField(blank=True)
    created_at = models.DateTimeField('Datetime created')

    def __str__(self):
        return '%s %s' % (self.name, self.points)




