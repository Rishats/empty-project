from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.db import connection



class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True)
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField('Datetime created')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
# Dev
def create_profile_database(sender, instance, **kwargs):
    if kwargs['created']:
        qn = connection.ops.quote_name
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE DATABASE %s" % (
                    qn(str(instance.user))))
            except Exception as e:
                print(e)

# Dev
def delete_profile_database(sender, instance, **kwargs):
    qn = connection.ops.quote_name
    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP DATABASE %s" % (
                qn(str(instance.user))))
        except Exception as e:
            print(e)

post_save.connect(create_profile_database, sender=Student)
pre_delete.connect(delete_profile_database, sender=Student)

class Work(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=255, blank=True)
    points = models.PositiveSmallIntegerField(blank=True)
    created_at = models.DateTimeField('Datetime created')

    def __str__(self):
        return '%s %s' % (self.name, self.points)

