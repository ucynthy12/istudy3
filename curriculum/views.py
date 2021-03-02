from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Course, Subject, Lesson
from django.urls import reverse_lazy
from .forms import LessonForm,LessonUpdateForm
from django.http import HttpResponseRedirect,FileResponse


def CourseListView(request):
  courses = Course.objects.all()
  return render(request,'course_list.html',{"courses":courses})

@login_required(login_url='login')
def SubjectsView(request,course_id):
  course=Course.objects.get(id=course_id)
  subjects = Subject.objects.filter(course=course)
  return render(request,'subject.html',{"course":course,"subjects":subjects})


def LessonsView(request,course_id,subject_id):
  course=Course.objects.get(id=course_id)
  subject=Subject.objects.get(id=subject_id)
  lessons=Lesson.objects.filter(subject=subject)
  return render(request,'lesson.html',{"course":course,"subjects":subject,"lessons":lessons})


def LessonDetailView(request,subject_id,lesson_id):
  subject=Subject.objects.get(id=subject_id)
  lesson=Lesson.objects.filter(subject=subject)
  print(lesson)
  return render(request,'lesson_details.html',{"subject":subject,"lesson":lesson})

def LessonCreateView(request,course_id,subject_id):
  course= Course.objects.get(id=course_id)
  subject=Subject.objects.get(id=subject_id)
  lesson = Lesson.objects.filter(subject=subject)
  if request.method == 'POST':
    form = LessonForm(request.POST, request.FILES)
    if form.is_valid():
      create= form.save(commit=False)
      create.created_by =request.user
      create.course = course
      create.subject = subject
      create.lesson=lesson
      create.save()
      return redirect('lessons-list',course.id,subject.id)
  else:
    form = LessonForm()
  return render(request,'lesson_create.html',{'form':form,'lesson':lesson,"subject":subject,'course':course})


def LessonUpdateView(request,subject_id,lesson_id):
  subject=Subject.objects.get(id=subject_id)
  lesson=Lesson.objects.filter(subject=subject)

  if request.method == 'POST':
    form = LessonUpdateForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
      return redirect('lesson-detail',subject.id,lesson.id)
  
  else:
    form= LessonUpdateForm()
  return render(request,'lesson_update.html',{"subject":subject,"lesson":lesson,'form':form})

def LessonDeleteView(request,subject_id,lesson_id):
  subject=Subject.objects.get(id=subject_id)
  lesson=Lesson.objects.filter(subject=subject)
  lesson.delete()
  return render(request,'lesson_delete.html',{"subject":subject,"lesson":lesson})






class CourseView(APIView):
  def get(self,request):
    courses=Course.objects.all()
    serializer=CourseSerializer(courses,many=True)
    return Response(serializer.data)

  def post(self):
    pass 

class SubjectsApiView(APIView):
  def get(self,request):
    subjects=Subject.objects.all()
    serializer=SubjectSerializer(subjects,many=True)
    return Response(serializer.data)

  def post(self):
    pass 

class LessonView(APIView):
  def get(self,request):
    lessons=Lesson.objects.all()
    serializer=LessonSerializer(lessons,many=True)
    return Response(serializer.data)

  def post(self):
    pass 

