from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [
    path('', views.CourseListView , name='course_list'),
    path('<course_id>/', views.SubjectsView , name='subjects-list'),
    path('<course_id>/<subject_id>/', views.LessonsView , name='lessons-list'),
    path('<course_id>/<subject_id>/add/', views.LessonCreateView,name='create'),
    path('<subject_id>/<lesson_id>',views.LessonDetailView,name='lesson-detail'),

]