from django.shortcuts import render

# Create your views here.
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Course, Subject, Lesson
from django.urls import reverse_lazy
from .forms import LessonForm
from django.http import HttpResponseRedirect


def CourseListView(request):
  courses = Course.objects.all()
  return render(request,'course_list.html',{"courses":courses})


def SubjectsView(request,course_id):
  course=Course.objects.get(id=course_id)
  subjects = Subject.objects.filter(course=course)
  print(subjects)
  return render(request,'subject.html',{"course":course,"subjects":subjects})


def LessonsView(request,course_id,subject_id):
  course=Course.objects.get(id=course_id)
  subject=Subject.objects.get(id=subject_id)
  lessons=Lesson.objects.filter(subject=subject)
  print(lessons)
  return render(request,'lesson.html',{"course":course,"subjects":subject,"lessons":lessons})


def LessonDetailView(request,subject_id,lesson_id):
  subject=Subject.objects.get(id=subject_id)
  lesson=Lesson.objects.get(id=lesson_id)
  return render(request,'lesson_details.html',{"subject":subject,"lesson":lesson})

