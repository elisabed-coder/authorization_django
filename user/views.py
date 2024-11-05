from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, logger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from .models import User, Teacher, Mark, Student
from .forms import UserRegisterForm, StudentSelectionForm
from django.http import JsonResponse
from django.utils.decorators import method_decorator



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
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            auth_login(request, user)

            # Redirect to a different form based on the role
            if user.role == User.Role.STUDENT:
                return redirect('user:home')
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
    user = request.user  # Get the logged-in user

    # Retrieve scores for the logged-in student, including subject names
    scores = Mark.objects.filter(student=user).select_related('subject')

    return render(request, 'home.html', {
        'user': user,
        'scores': scores
    })

def student_list(request):
    students = User.objects.filter(role=User.Role.STUDENT)
    return render(request, 'student_list.html', {'students': students})

def teacher_list(request):
    teachers = User.objects.filter(role=User.Role.TEACHER)
    return render(request, 'teacher_list.html', {'teachers': teachers})


@login_required
def select_teacher_subject(request):
    logger.info(f"Method: {request.method}")
    logger.info(f"User: {request.user.username}")

    if request.method == 'POST':
        logger.info(f"POST data: {request.POST}")
        form = StudentSelectionForm(request.POST, instance=request.user)

        try:
            if form.is_valid():
                logger.info(f"Form is valid. Cleaned data: {form.cleaned_data}")

                # Get the selected teacher instance
                selected_teacher = form.cleaned_data['selected_teacher']  # This should be the Teacher instance

                subject = form.cleaned_data['subject']

                # Update user
                user = form.save(commit=False)
                user.subject = subject
                user.selected_teacher = selected_teacher
                user.role = User.Role.STUDENT
                user.save()

                logger.info(f"User saved successfully. Subject: {user.subject}, Teacher: {user.selected_teacher.username}")
                messages.success(request, 'Your selection has been saved successfully.')
                return redirect('user:home')
            else:
                logger.error(f"Form validation failed. Errors: {form.errors}")
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            logger.exception("Error saving form")
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = StudentSelectionForm(instance=request.user)
        logger.info(f"Initialized GET form for user: {request.user.username}")

    context = {
        'form': form,
        'user': request.user,
        'debug': True
    }
    return render(request, 'teacher_list.html', context)

@require_http_methods(["GET"])
def get_teachers_by_subject(request):
    subject = request.GET.get('subject')
    logger.info(f"Fetching teachers for subject: {subject}")

    try:
        # Filter by subject and role
        teachers = Teacher.objects.filter(subject=subject, role=User.Role.TEACHER).values('id', 'username')
        logger.info(f"Found teachers: {list(teachers)}")
        return JsonResponse(list(teachers), safe=False)
    except Exception as e:
        logger.exception("Error fetching teachers")
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def delete_subject_selection(request):
    if request.user.is_authenticated:
        # Clear both the selected subject and teacher for the user
        request.user.subject = None
        request.user.selected_teacher = None  # Assuming selected_teacher is a field on the user model
        request.user.save()
        return JsonResponse({'message': 'Subject and teacher selection deleted successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)


class MarkListView(View):
    @staticmethod
    def get(request, student_id):
        teacher = request.user
        student = get_object_or_404(Student, id=student_id)

        # Filter marks for the selected student
        marks = Mark.objects.filter(student=student)

        context = {
            'student': student,
            'marks': marks,
            'teacher': teacher,
        }
        return render(request, 'mark_list.html', context)

class MarkCreateView(View):
    @staticmethod
    def post(request, student_id):
        student = get_object_or_404(Student, id=student_id)
        subject = request.POST.get('subject')  # This is now hidden
        mark_value = request.POST.get('mark')

        # Create or update the mark
        Mark.objects.update_or_create(
            student=student,
            subject=subject,
            defaults={'mark': mark_value, 'teacher': request.user}
        )

        return redirect('user:mark_list', student_id=student.id)


@method_decorator(login_required, name='dispatch')
class MyStudentsView(View):
    def get(self, request):
        teacher = request.user
        students = Student.objects.filter(selected_teacher=teacher)

        context = {
            'students': students,
        }
        return render(request, 'my_students.html', context)
