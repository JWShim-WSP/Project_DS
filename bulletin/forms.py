from django import forms
from .models import Bulletin, Comment
from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Textarea, DateTimeInput, DateInput, Select
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields= ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content','parent']
        labels = {
            'content': _(''),
        }

        widgets = {
            'content' : forms.TextInput(),
        }
