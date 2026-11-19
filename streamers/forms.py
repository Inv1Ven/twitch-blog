from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Ваше имя")
    email = forms.EmailField(label="Ваш Email")
    to = forms.EmailField(label="Кому отправить (Email)")
    comments = forms.CharField(required=False, widget=forms.Textarea, label="Комментарий к письму")