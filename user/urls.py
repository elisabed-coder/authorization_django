from django.urls import path
from . import views

app_name = 'user'  # This defines the namespace for this app

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:user_id>/', views.student_profile, name='student_profile'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:user_id>/', views.teacher_profile, name='teacher_profile'),
    path('logout/', views.logout_view, name='logout'),
]
