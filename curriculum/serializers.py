from rest_framework import serializers
from .models import Course,Subject,Lesson

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields =('__all__')

class SubjectSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model=Subject
        fields =('name','course','image','description')
class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    subject = SubjectSerializer()
    class Meta:
        model=Lesson

        fields =('lesson_id','course','created_by','created_at','subject','name','position','video','ppt','notes')