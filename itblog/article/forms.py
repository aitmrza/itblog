from django import forms
from .models import *

class ArticleForm(forms.ModelForm):
    tags = forms.CharField(max_length=125, required=False)
    class Meta:
        model = Article
        fields = ['title', 'text', 'picture', 'tag', 'tags']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']