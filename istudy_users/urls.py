from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register,name='signup'),
    path('user_login/',views.user_login,name='login'),
    path('user_logout/',views.user_logout,name='logout'),
    path('api/register/', views.registration_view, name='register'),
    path('api/login/', obtain_auth_token, name='loginApi'),
    path('users/',views.usersList.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),


]
# if settings.DEBUG:
#     urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)