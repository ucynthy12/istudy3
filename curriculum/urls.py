from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [
    path('', views.CourseListView , name='course_list'),
    path('<course_id>/', views.SubjectsView, name='subjects-list'),
    path('<course_id>/<subject_id>', views.LessonsView , name='lessons-list'),
    path('<course_id>/<subject_id>/add/', views.LessonCreateView,name='create'),
    path('<subject_id>/<lesson_id>/',views.LessonDetailView,name='lesson-detail'),
    path('<subject_id>/<lesson_id>/update/',views.LessonUpdateView,name='lesson-update'),
    # path('<subject_id>/<lesson_id>/delete/',views.LessonDeleteView,name='lesson-delete'),
    path('1/api/courses/',views.CourseView.as_view()),
    path('1/api/subjects/',views.SubjectsApiView.as_view()),
    path('1/api/lessons/',views.LessonView.as_view()),

]