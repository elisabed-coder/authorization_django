from django.urls import path
from . import views

app_name = 'user'  # This defines the namespace for this app

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('teachers/', views.select_teacher_subject,  name='select_teacher_subject'),
    path('select-teacher-subject/', views.select_teacher_subject, name='select_teacher_subject'),
    path('get-teachers/', views.get_teachers_by_subject, name='get_teachers_by_subject'),  # Add this line
    path('logout/', views.logout_view, name='logout'),
    path('delete_subject_selection/', views.delete_subject_selection, name='delete_subject_selection'),

]
