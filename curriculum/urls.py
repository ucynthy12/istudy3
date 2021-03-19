from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [
    path('',views.CourseListView,name='course_list'),
    path('<course_id>/', views.SubjectsView ,name='subjects-list'),
    path('<course_id>/lesson/<subject_id>/', views.LessonsView , name='lessons-list'),
    path('<course_id>/<subject_id>/add/', views.LessonCreateView,name='create'),
    path('subject/<subject_id>/<lesson_id>/',views.LessonDetailView,name='lesson-detail'),
    path('<subject_id>/<lesson_id>/update/',views.LessonUpdateView,name='lesson-update'),
    path('lesson/<int:pk>/delete/',views.LessonDeleteView.as_view(),name='lesson-delete'),
    path('1/api/courses/',views.CourseView.as_view()),
    path('1/api/subjects/',views.SubjectsApiView.as_view()),
    path('1/api/lessons/',views.LessonView.as_view()),
    path('1/<course_id>/payment/', views.payment, name='payment'),
    path('<course_id>/<order_id>/',views.Order),
    path('1/api/course_paid/',views.CoursePaidApiView.as_view()),

]