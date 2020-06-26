from django import forms

class PostForm(forms.Form):
    header = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)