from django import forms

from profiles.models import ProfileUser


class ProfileForms(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['user', 'full_name', 'bio', 'profile_picture']
