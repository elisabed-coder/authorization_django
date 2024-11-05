from django import forms
from user.models import User, Teacher
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']  # Removed 'subject' from fields


class StudentSelectionForm(forms.ModelForm):
    subject = forms.ChoiceField(
        choices=User.SubjectChoices.choices,
        required=True,
        label="Select Subject",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_subject'
        })
    )
    selected_teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.none(),
        required=True,
        label="Select Teacher",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_selected_teacher'
        })
    )

    class Meta:
        model = User
        fields = ['subject', 'selected_teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize queryset to only teachers
        self.fields['selected_teacher'].queryset = Teacher.objects.filter(role=User.Role.TEACHER)

        # Filter teachers by subject if subject is specified
        if self.data.get('subject'):
            self.fields['selected_teacher'].queryset = Teacher.objects.filter(
                subject=self.data.get('subject'),
                role=User.Role.TEACHER
            )
        elif self.instance and self.instance.subject:
            self.fields['selected_teacher'].queryset = Teacher.objects.filter(
                subject=self.instance.subject,
                role=User.Role.TEACHER
            )
