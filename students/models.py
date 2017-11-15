from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
from django import forms
import random, string


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, verbose_name="Логин")
    first_name = models.CharField(max_length=80, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=80, blank=True, verbose_name="Фамилия")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Студента'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


def password_generate(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def create_profile_database(sender, instance, **kwargs):
    if kwargs['created']:
        qn = connection.ops.quote_name
        password = password_generate(20)
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci;" % (qn(str(instance.user))))
                cursor.execute("CREATE USER %s@localhost IDENTIFIED BY '%s';"
                               % (qn(str(instance.user)), str(password)))
                cursor.execute("GRANT ALL PRIVILEGES ON %s.* TO %s@localhost WITH GRANT OPTION;"
                               % (qn(str(instance.user)), qn(str(instance.user))))
            except Exception as e:
                print(e)
        body = 'Пользователь: %(db)s База данных: %(db)s Пароль: %(password)s'
        send_mail('[ST | Platform] Ваш доступ к СУБД!',
                  body % {"db": instance.user, "password": password},
                  settings.EMAIL_HOST_USER,
                  [instance.user.email], fail_silently=False)


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
    body = 'Вашу базу удалил преподаватель и Вы теперь не числитесь в студентах ST-Platform: База данных: %(db)s'
    send_mail('[ST | Platform] Ваша база в СУБД была удалена!',
              body % {"db": instance.user},
              settings.EMAIL_HOST_USER,
              [instance.user.email], fail_silently=False)


post_save.connect(create_profile_database, sender=Student)
pre_delete.connect(delete_profile_database, sender=Student)


class Work(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    name = models.CharField(max_length=80, blank=True, verbose_name="Название")
    description = models.CharField(max_length=255, blank=True, verbose_name="Описание")
    points = models.PositiveSmallIntegerField(blank=True, verbose_name="Баллы")
    done = models.NullBooleanField(verbose_name="Выполнение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи для студентов'

    def __str__(self):
        return '%s получил задание %s на %s баллов' % (self.student, self.name, self.points)


class PasswordDatabase(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, verbose_name="Логин")
    password = models.CharField(max_length=80, blank=True, verbose_name="Пароль")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'новый пароль'
        verbose_name_plural = 'Логи изменений паролей'

    def __str__(self):
        return 'Пароль для базы "%s" был изменен' % self.user


def change_password_database(sender, instance, **kwargs):
        qn = connection.ops.quote_name
        with connection.cursor() as cursor:
            try:
                cursor.execute("SET PASSWORD FOR %s@localhost = PASSWORD('%s');" % (qn(str(instance.user)), str(instance.password)))
            except Exception as e:
                print(e)
        body = 'Пользователь: %(db)s База данных: %(db)s Пароль: %(password)s'
        send_mail('[ST | Platform] Ваш пароль от СУБД был сброшен!',
                  body % {"db": instance.user, "password": instance.password},
                  settings.EMAIL_HOST_USER,
                  [instance.user.email], fail_silently=False)


post_save.connect(change_password_database, sender=PasswordDatabase)



