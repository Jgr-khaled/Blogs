from django import forms 
from .models import User, Comment, Post


class UserForm(forms.Form):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
    
    
class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['topic', 'author', 'title', 'body', 'image' ]
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']
        
class SearchForm(forms.Form):
    query = forms.CharField()