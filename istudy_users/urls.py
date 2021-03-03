from . import views
from django.urls import path,include

from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('register/',views.register,name='signup'),
    path('user_login/',views.user_login,name='login'),
    path('user_logout/',views.user_logout,name='logout'),
    path('api/register/', views.registration_view, name='register'),
    path('api/login/', obtain_auth_token, name='loginApi'),
    path('users/',views.usersList.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<username>/', views.profile, name='profile'),
    path('api/token/login/',views.LoginView.as_view()),


]
