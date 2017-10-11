from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField('Datetime created')

class Work(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=255, blank=True)
    points = models.PositiveSmallIntegerField(blank=True)
    created_at = models.DateTimeField('Datetime created')

