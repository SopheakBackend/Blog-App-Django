from django import forms
from .models import Comment
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length= 25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(max_length=250, required=False, widget=forms.Textarea)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'body',
        ]
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)