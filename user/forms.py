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
        # Initialize with all teachers if no subject is selected
        self.fields['selected_teacher'].queryset = Teacher.objects.all()

        # If there's initial data with a subject, filter teachers
        if self.data.get('subject'):
            self.fields['selected_teacher'].queryset = Teacher.objects.filter(
                subject=self.data.get('subject')
            )
        elif self.instance and self.instance.subject:
            self.fields['selected_teacher'].queryset = Teacher.objects.filter(
                subject=self.instance.subject
            )

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        selected_teacher = cleaned_data.get('selected_teacher')

        if subject and selected_teacher:
            if selected_teacher.subject != subject:
                raise forms.ValidationError(
                    "Selected teacher does not teach the selected subject."
                )
        return cleaned_data