from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STUDENT = 'STUDENT', 'Student'
        TEACHER = 'TEACHER', 'Teacher'

    class SubjectChoices(models.TextChoices):
        MATH = 'MATH', 'Math'
        ENGLISH = 'ENGLISH', 'English'
        ENGINEERING = 'ENGINEERING', 'Engineering'
        SCIENCE = 'SCIENCE', 'Science'
        HISTORY = 'HISTORY', 'History'

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    subject = models.CharField(max_length=100, choices=SubjectChoices.choices, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Students"

@receiver(post_save, sender=Student)
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)

class Teacher(User):
    base_role = User.Role.TEACHER
    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Teachers"

