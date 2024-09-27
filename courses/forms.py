from .models import Course, Lesson, Module
from django import forms






class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Corrected to pass *args and **kwargs to parent class
        # Set the queryset for the course field to all courses
        self.fields['course'].queryset = Course.objects.all()