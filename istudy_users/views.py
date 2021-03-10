from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from .serialisers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
from .permissions import IsAdminOrReadOnly
from .email import send_welcome_email
from django.contrib import messages
from curriculum.models import Course
import jwt
from django.conf import settings
from django.contrib import auth


def index(request):
    courses = Course.objects.all()
    return render(request,'home.html',{"courses":courses})
def about(request):
    courses = Course.objects.all()
    return render(request,'about.html',{"courses":courses})    

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            email = user_form.cleaned_data['email']
            user = authenticate(username=username,password=password)
            login(request,user)

            messages.success(request, f'Your account has been created, you can now login!')
            # messages.success(request, f'Account created for {username}!')
            send_welcome_email(username,email)
            registered =True
            return redirect('index')
            

        else:
            for msg in user_form.error_messages:
                messages.error(request, f"{msg}: {user_form.error_messages[msg]}")
            print(msg)
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render(request,'registration/registration_form.html',{'registered':registered,'user_form':user_form,})


def user_login(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
    
    return render(request,'registration/login.html',{'form':form,'title':title})

    # if request.method == "POST":
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     user = authenticate(username=username,password=password)

    #     if user:
    #         if user.is_active:
    #             login(request,user)
    #             return HttpResponseRedirect(reverse('index'))
            
    #         else:
    #             return HttpResponse('ACCOUNT IS DEACTIVATED')

    #     else:
    #         return HttpResponse('Please use correct id and password')

    # else:
    #     return render(request,'registration/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

class usersList(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request):
        users = User.objects.all()
        serializer= UserDetailsSerializer(users,many=True)

        return Response(serializer.data)

@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':

        serializer = RegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['full_name'] = user.full_name
            data['phone_number'] = user.phone_number


            # token = Token.objects.get(user=user).key
            # data['token'] = token

        else:
            data = serializer.errors
            print(data)
        return Response(data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode(
                {'id':user.pk,'username': user.username,'email':user.email,'full_name':user.full_name,'phone_number':user.phone_number,'role':user.role}, settings.JWT_SECRET_KEY)

            serializer = UserDetailsSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@login_required(login_url='login')
def profile(request, username):

    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
           
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    
    return render(request, 'registration/profile.html',{'user_form': user_form, 'profile_form': profile_form,})