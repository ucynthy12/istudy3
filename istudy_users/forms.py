from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=300,help_text='Required. Inform a valid email address')
    parent = 'parent'
    student = 'student'
    taecher = 'teacher'
    
    roles=[
        ('parent','parent'),
        ('student','student'),
    ]
    role = forms.ChoiceField(required=True,choices=roles)
    class Meta():
        model = User
        fields = ('full_name','username', 'email','role','phone_number','password1', 'password2',)

        labels ={
            'password1':'Password',
            'password2': 'Confirm Password',
        }

class UpdateUserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [ 'profile_picture', 'bio']

  