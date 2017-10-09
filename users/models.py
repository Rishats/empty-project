from django.db import models


class Student(models.Model):
    lname = models.CharField(max_length=256)
    fname = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    created_at = models.DateTimeField('Datetime created')

