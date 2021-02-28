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
  lesson=Lesson.objects.filter(subject=subject)
  return render(request,'lesson_details.html',{"subject":subject,"lesson":lesson})

def LessonCreateView(request,course_id,subject_id):
  course= Course.objects.get(id=course_id)
  subject=Subject.objects.get(id=subject_id)
  lesson = Lesson.objects.filter(subject=subject)
  if request.method == 'POST':
    form = LessonForm(request.POST, request.FILES)
    if form.is_valid():
      create= form.save(commit=False)
      create.created_by = self.request.user
      create.course = course
      create.subject = subject
      create.lesson=lesson
      create.save()
      return redirect('lessons-list',course.id,subject.id)
  else:
    form = LessonForm()
  return render(request,'lesson_create.html',{'form':form,'lesson':lesson,"subject":subject,'course':course})

# form_class = LessonForm
#     context_object_name = 'subject'
#     model= Subject
#     template_name = 'curriculum/lesson_create.html'
#     def get_success_url(self):
#         self.object = self.get_object()
#         standard = self.object.standard
#         return reverse_lazy('curriculum:lesson_list',kwargs={'standard':standard.slug,
#                                                              'slug':self.object.slug})
#     def form_valid(self, form, *args, **kwargs):
#         self.object = self.get_object()
#         fm = form.save(commit=False)
#         fm.created_by = self.request.user
#         fm.Standard = self.object.standard
#         fm.subject = self.object
        # fm.save()
        # return HttpResponseRedirect(self.get_success_url())