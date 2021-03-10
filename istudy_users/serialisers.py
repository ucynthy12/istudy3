from rest_framework import serializers
from allauth.account.adapter import get_adapter
from istudy_project import settings
from .models import User
from allauth.account.utils import setup_user_email

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'full_name','role','phone_number')
        read_only_fields = ('email', )

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
  
    class Meta:

        model = User
        fields = ('id', 'full_name','username', 'email', 'role', 'phone_number',  'password','password2')
        extra_kwargs = {
            'password': {'write_only': True}
            }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            full_name=self.validated_data['full_name'],
            phone_number=self.validated_data['phone_number'],
            role=self.validated_data['role'],



        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
           raise serializers.ValidationError({'password':'Passwords must macth.!'})

        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = User
        fields = ['username', 'password']