from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail


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


def create_profile_database(sender, instance, **kwargs):
    if kwargs['created']:
        qn = connection.ops.quote_name
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE DATABASE %s;" % (qn(str(instance.user))))
                cursor.execute("CREATE USER %s@localhost IDENTIFIED BY '%s';"
                               % (qn(str(instance.user)), str(instance.user)))
                cursor.execute("GRANT ALL PRIVILEGES ON %s.* TO %s@localhost WITH GRANT OPTION;"
                               % (qn(str(instance.user)), qn(str(instance.user))))
            except Exception as e:
                print(e)


def delete_profile_database(sender, instance, **kwargs):
    qn = connection.ops.quote_name
    with connection.cursor() as cursor:
        try:
            cursor.execute("DROP DATABASE %s" % (
                qn(str(instance.user))))
            cursor.execute("DROP user %s@'localhost'" % (
                qn(str(instance.user))))
            cursor.execute("flush privileges;")
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


class PasswordDatabase(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True)
    password = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField('Datetime created')

    def __str__(self):
        return '%s %s' % (self.user, 'DB PASS CHANGED')


def change_password_database(sender, instance, **kwargs):
        qn = connection.ops.quote_name
        with connection.cursor() as cursor:
            try:
                cursor.execute("SET PASSWORD FOR %s@localhost = PASSWORD('%s');" % (qn(str(instance.user)), str(instance.password)))
            except Exception as e:
                print(e)
        body = 'DB: %(db)s Password: %(password)s'
        send_mail('[ST | Platform] New DB password!',
                  body % {"db": instance.user, "password": instance.password},
                  settings.EMAIL_HOST_USER,
                  [instance.user.email], fail_silently=False)


post_save.connect(change_password_database, sender=PasswordDatabase)



