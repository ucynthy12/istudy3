from django import forms
from .models import Lesson,User,Comment
from mptt.forms import TreeNodeChoiceField
from cloudinary.forms import CloudinaryFileField


class LessonForm(forms.ModelForm):
    video = CloudinaryFileField(
    options = { 
      'tags': "directly_uploaded",
      'crop': 'limit', 'width': 1000, 'height': 1000,
     'eager': [
    { "width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
    { "width": 160, "height": 100, "crop": "crop", "gravity": "south",
        "audio_codec": "none"}],
    })
    class Meta:
        model = Lesson
        fields = ('lesson_id','name','video','ppt','notes')
        exclude = ['created_by','course','subject']

class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model =Lesson
        fields = ('__all__')
        exclude = ['created_by','course','subject']

class CommentForm(forms.ModelForm):
    parent=TreeNodeChoiceField(queryset=Comment.objects.all())
    

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)


        self.fields['parent'].widget.attrs.update(
            {'class':'d-none'})
        self.fields['parent'].label = ''

        self.fields['parent'].required=False
        
    class Meta:
        model = Comment
        labels = {"content":"Comment:"}
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':70, 'placeholder':"Enter Your Comment"}),
        }
        fields = ('author','content','parent')
        exclude = ['author']


        
