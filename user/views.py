from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, StudentProfile, TeacherProfile
from .forms import UserRegisterForm, StudentSelectionForm

def login_view(request):
    selected_role = request.GET.get('role')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = request.POST.get('role')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.role == role:
                    auth_login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('user:home')
                else:
                    messages.error(request, 'Invalid role. Please select the correct role.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'selected_role': selected_role
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('user:home')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user:login_view')
@login_required
def home(request):
    return render(request, 'home.html')

def student_list(request):
    students = User.objects.filter(role=User.Role.STUDENT)
    return render(request, 'student_list.html', {'students': students})

def student_profile(request, user_id):
    student = get_object_or_404(StudentProfile, user_id=user_id)
    return render(request, 'student_profile.html', {'student': student})

def teacher_list(request):
    teachers = User.objects.filter(role=User.Role.TEACHER)
    return render(request, 'teacher_list.html', {'teachers': teachers})

def teacher_profile(request, user_id):
    teacher = get_object_or_404(TeacherProfile, user_id=user_id)
    return render(request, 'teacher_profile.html', {'teacher': teacher})


def select_teacher_subject(request):
    if request.method == 'POST':
        form = StudentSelectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = StudentSelectionForm()

    # Retrieve teachers list to display in template
    teachers = User.objects.filter(role=User.Role.TEACHER)
    return render(request, 'teacher_list.html', {'form': form, 'teachers': teachers})