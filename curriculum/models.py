from django.db import models
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify
from istudy_users.models import User
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(null=True,blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class Subject(models.Model):
    subject_id=models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='subjects')
    image= CloudinaryField('image',null=True,blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args,**kwargs)

def save_lesson_files(instance,filename):
    upload_to ='Images/'
    ext = filename.split('.')[-1]

    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(instance.lesson_id,instance.lesson_id,ext)

        if os.path.exists(filename):
            new_name = str(instance.lesson_id)+ str('1')
            filename = 'lesson_images/{}/{}.{}'.format(instance.lesson_id,new_name,ext)

    return os.path.join(upload_to,filename)
        


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100,unique=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='lessons')
    name = models.CharField(max_length=300)
    position = models.PositiveSmallIntegerField(verbose_name='Chapter no.')
    slug = models.SlugField(null=True,blank=True)
    video= models.FileField(upload_to=save_lesson_files,verbose_name='Video',blank=True,null=True)
    ppt = models.FileField(upload_to=save_lesson_files,verbose_name='Presentation',blank=True)
    notes = models.FileField(upload_to=save_lesson_files,verbose_name='Notes',blank=True)

    class Meta:
        ordering = ['position']


    def __str__(self):
        return self.name


    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)


    
    