from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Course, Subject, Lesson,Comment
from django.urls import reverse_lazy
from .forms import LessonForm,LessonUpdateForm,CommentForm,ReplyForm
from django.http import HttpResponseRedirect,FileResponse
from django.views.generic import DeleteView


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
  # print(lesson)
  comments= Comment.objects.filter(lesson_name=lesson,reply=None).order_by('-id')
  if request.method == 'POST':
    comment_form = CommentForm(request.POST,request.FILES or None)
    if comment_form.is_valid():
      body = request.data.get('body')
      print(body)
      reply_id = request.data.get('comment_id')
      print(reply_id)
      comment_qs =None
      if reply_id:
        comment_qs = Comment.objects.get(id=reply_id)
      comment = Comment.objects.create(lesson_name=lesson,author=request.user,body=body,reply=comment_qs)
      comment.save()
      return redirect('curriculum:lesson-detail',subject.id,lesson.id)
  else:
    comment_form = CommentForm()

  return render(request,'lesson_details.html',{"subject":subject,"lesson":lesson,'comment_form':comment_form})

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
      return redirect('lesson-detail',subject.id,lesson.id)
  
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

class LessonDetailView(DetailView, FormView):

  context_object_name = 'lessons'
  model = Lesson
  template_name = 'curriculum/lesson_details.html'
  form_class = CommentForm
  second_form_class = ReplyForm    
  def get_context_data(self, **kwargs):
    context = super(LessonDetailView, self).get_context_data(**kwargs)
    if 'form' not in context:
      context['form'] = self.form_class(request=self.request)
      if 'form2' not in context:
      context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
      return context   
        
  def post(self, request, *args, **kwargs):
     self.object = self.get_object()
     if 'form' in request.POST:
       form_class = self.get_form_class()
         form_name = 'form'
     else:
       form_class = self.second_form_class
       form_name = 'form2'       
       form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)        if form_name=='form' and form.is_valid():
       print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail',kwargs={'standard':standard.slug,
                                                             'subject':subject.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())