from django.shortcuts import render
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

def index(request):
    return render(request,'home.html')


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            registered =True

        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()

    return render(request,'registration/registration_form.html',{'registered':registered,'user_form':user_form,})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('ACCOUNT IS DEACTIVATED')

        else:
            return HttpResponse('Please use correct id and password')

    else:
        return render(request,'registration/login.html')

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
    def post(self,request):
        data = request.data
        username = data.get('username','')
        password = data.get('password','')
        user = auth.authenticate(username=username,password=password)

        if user:
            auth_token = jwt.encode({'username':user.username},settings.JWT_SECRET_KEY)

            serializer = UserSerializer(user,many=True)  

            data = {
                'user':serializer.data,'token':auth_token
            }   
        return Response(data,status=status.HTTP_200_OK)


        return Response({'detail':'Invalid Credentitials'},status=status.HTTP_401_UNAUTHORIZED)