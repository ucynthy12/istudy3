from django.contrib import admin
from .models import User
from curriculum.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Reply)

