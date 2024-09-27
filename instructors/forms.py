
from django import forms
from django.forms.models import inlineformset_factory

from courses.models import Course, Lesson, Module




ModuleFormSet = inlineformset_factory(
                Course,
                Module,
                fields=['title'],
                extra=2,
                can_delete=True
)


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'module', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
