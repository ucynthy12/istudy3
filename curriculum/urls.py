from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [
    path('', views.CourseListView , name='course_list'),
    path('<course_id>/', views.SubjectsView , name='subjects-list'),
    path('<course_id>/<subject_id>/', views.LessonsView , name='lessons-list'),
    path('<subject_id>/<lesson_id>', views.LessonDetailView , name='lesson-detail'),
    # path('<str:course>/<str:slug>/create/', views.LessonCreateView ,name='lesson-create'),
    # path('<str:course>/<str:subject>/<slug:slug>/', views.LessonDetailView,name='lesson-detail'),
    # path('<str:course>/<str:subject>/<slug:slug>/update/', views.LessonUpdateView,name='lesson-update'),
    # path('<str:course>/<str:subject>/<slug:slug>/delete/', views.LessonDeleteView,name='lesson-delete'),

]