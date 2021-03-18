from rest_framework import serializers
from .models import Course,Subject,Lesson,CoursePayment
from istudy_users.serialisers import UserDetailsSerializer
class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Course
        fields =('__all__')

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model=Subject
        fields =('name','course','image','description')
class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    subject = SubjectSerializer()
    class Meta:
        model=Lesson

        fields =('lesson_id','course','created_by','created_at','subject','name','position','video','ppt','notes')

class CoursePaidSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    user = UserDetailsSerializer()

    class Meta:
        model=CoursePayment
        fields = ('user','course','order_id','paid')
