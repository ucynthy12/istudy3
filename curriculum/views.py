from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Course, Subject, Lesson,Comment
from django.urls import reverse_lazy
from .forms import LessonForm,LessonUpdateForm,CommentForm
from django.http import HttpResponseRedirect,FileResponse
from django.views.generic import DeleteView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


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
  lesson=Lesson.objects.get(id=lesson_id)
  print(lesson)
  allcomments= Comment.objects.filter(lesson=lesson).order_by('id')
  page = request.GET.get('page',1)
  paginator = Paginator (allcomments,3)

  try:
    comments = paginator.page(page)
  except PageNotAnInteger:
    comments = paginator.page(1)
  except EmptyPage:
    comments = paginator.page(paginator.num_pages)




  user_comment = None
  if request.method == 'POST':
    comment_form = CommentForm(request.POST,request.FILES or None)
    if comment_form.is_valid():
      user_comment = comment_form.save(commit=False)
      user_comment.lesson = lesson
      user_comment.save()
      return redirect('curriculum:lesson-detail',subject.id,lesson.id)
  else:
    comment_form = CommentForm()

  return render(request,'lesson_details.html',{"subject":subject,"lesson":lesson,'comment_form':comment_form,'comments':comments,'allcomments': allcomments,})

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
      return redirect('curriculum:lessons-list',course.id,subject.id)
  else:
    form = LessonForm()
  return render(request,'lesson_create.html',{'form':form,'lesson':lesson,"subject":subject,'course':course})


def LessonUpdateView(request,subject_id,lesson_id):
  subject=Subject.objects.get(id=subject_id)
  lesson=Lesson.objects.get(id=lesson_id)

  if request.method == 'POST':
    form = LessonUpdateForm(request.POST,request.FILES,instance=lesson)
    if form.is_valid():
      form.save()
      return redirect('curriculum:lesson-detail',subject.id,lesson.id)
  
  else:
    form= LessonUpdateForm(instance=lesson)
  return render(request,'lesson_update.html',{"subject":subject,"lesson":lesson,'form':form})

class LessonDeleteView(DeleteView):
  model = Lesson
  template_name = "lesson_delete.html"


  def get_success_url(self):
        return reverse_lazy('curriculum:course_list')












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

