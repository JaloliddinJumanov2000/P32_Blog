from django.forms import ModelForm
from blog.models import Blog, Comment
from django import forms


class BlogForms(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('author',)


from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }

