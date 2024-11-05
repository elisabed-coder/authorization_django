from django.contrib import admin
from .models import User, Student, Teacher

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'subject')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('subject',)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'subject')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('subject',)

# Register your models
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
