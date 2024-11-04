# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import StudentProfile, Teacher, User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'subject']


class StudentSelectionForm(forms.ModelForm):
    selected_subject = forms.ChoiceField(
        choices=User.SubjectChoices.choices,
        required=True,
        label="Select Subject"
    )

    class Meta:
        model = StudentProfile
        fields = ['selected_subject']

    # Adding the teachers list manually for template display
    # def __init__(self, *args, **kwargs):
    #     super(StudentSelectionForm, self).__init__(*args, **kwargs)
    #     self.fields['teachers_list'] = User.objects.filter(role=User.Role.TEACHER)