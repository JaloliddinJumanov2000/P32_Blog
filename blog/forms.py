from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Comment
from blog.models import Blog, Comment
from django import forms


class BlogForms(ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'photo', 'type', 'published')
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'})
        }
