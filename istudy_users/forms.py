from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from cloudinary.forms import CloudinaryFileField
from django.contrib.auth import authenticate,login,logout

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=300,help_text='Required. Inform a valid email address')
    # parent = 'parent'
    # student = 'student'
    # taecher = 'teacher'
    
    # roles=[
    #     ('parent','parent'),
    #     ('student','student'),
    #     ('teacher','teacher'),
    # ]
    # role = forms.ChoiceField(required=True,choices=roles)
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


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'id':'user-password'
            
            }
        )
    )
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError('This is an invid user.')
        return username

class SignUpForm(UserCreationForm):
    full_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField(required=True)
    phone_number = forms.CharField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'id':'user-password'
            
            }
        )
    )
    password2 = forms.CharField(
        label = 'Confirm Password',

        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'id':'user-password'
            
            }
        )
    )
   
    class Meta():
        model = User
        fields = ('full_name','username', 'email','phone_number','role','password1', 'password2')
   

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError('This is an invalid username,please pick another.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('This email is already in use')
        return email

    