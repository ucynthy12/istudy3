from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from cloudinary.forms import CloudinaryFileField
from django.contrib.auth import authenticate,login,logout

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=300,help_text='Required. Inform a valid email address')
    parent = 'parent'
    student = 'student'
    taecher = 'teacher'
    
    roles=[
        ('parent','parent'),
        ('student','student'),
        ('teacher','teacher'),
    ]
    role = forms.ChoiceField(required=True,choices=roles)
    class Meta():
        model = User
        fields = ('full_name','username', 'email','role','phone_number','password1', 'password2',)

        labels ={
            'password1':'Password',
            'password2': 'Confirm Password',
        }

  
class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(
     options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
      'eager': [{ 'crop': 'fill', 'width': 150, 'height': 100 }]
    })
    class Meta:

        model = Profile
        fields = [ 'profile_picture', 'bio']


# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self,*args,**kwargs):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         user = authenticate(username=username,password=password)
#         if not user:
#             raise forms.ValidationError('this user does not exist')
#         if not user.check_password(password):
#             raise forms.ValidationError('Incorrect password')

#         if not user.is_active:
#             raise forms.ValidationError('This user is not longer active.')
#         return super(UserLoginForm,self).clean(*args,**kwargs)